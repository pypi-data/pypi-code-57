import ast
import os

import git


def repo_has_same_ast(git_dir: str, logger) -> bool:
    try:
        repo = git.Repo(git_dir, search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        raise ValueError(f'Not a git dir nor any of its parents: {os.path.abspath(git_dir)}')
    logger.info(f'Analysing {repo.git_dir}')
    if repo.is_dirty():
        logger.info('Repo is dirty, comparing uncommitted changes.')
        file_strategy = dirty_files_strategy
    else:
        logger.info(f'Repo is clean, comparing changes in latest commit ({repo.head.object.hexsha}).')
        file_strategy = lastcommit_files_strategy
    num_files_diff = num_files_different(repo, file_strategy, logger)
    logger.info(f'Found {num_files_diff} AST differences.')
    if num_files_diff:
        return False
    else:
        return True


def num_files_different(repo: git.Repo, file_strategy, logger) -> int:
    num_ast_diffs = 0
    for path, source_original, source_modified in file_strategy(repo):
        if not have_equal_ast(source_original, source_modified):
            logger.warn(f'AST does not match for {path}')
            num_ast_diffs += 1
        else:
            logger.info(f'AST matches for {path}')
    return num_ast_diffs


def lastcommit_files_strategy(repo: git.Repo):
    for item in repo.index.diff('HEAD~1').iter_change_type('M'):
        path = item.a_path
        if path.endswith('.py'):
            yield path, repo.git.show(f'HEAD~1:{path}'), repo.git.show(f'HEAD:{path}')


def dirty_files_strategy(repo: git.Repo):
    for item in repo.index.diff(None):
        path = item.a_path
        if not path.endswith('.py'):
            continue
        source_original = repo.git.show(f'HEAD:{path}')
        with open(os.path.join(repo.working_dir, path)) as modified:
            source_modified = modified.read()
        yield path, source_original, source_modified


def have_equal_ast(source1: str, source2: str) -> bool:
    try:
        dump1 = ast.dump(ast.parse(source1))
        dump2 = ast.dump(ast.parse(source2))
    except SyntaxError:
        return False
    return dump1 == dump2
