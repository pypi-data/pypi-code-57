import unittest

from shipa.gitignore import get_pattern_from_line, GitIgnore


class GetPatternFromLineTestCase(unittest.TestCase):

    def test_negative(self):
        _, negative = get_pattern_from_line(line='!env3')
        self.assertTrue(negative)
        _, negative = get_pattern_from_line(line='    !env3')
        self.assertTrue(negative)
        _, negative = get_pattern_from_line(line='    !  env3')
        self.assertTrue(negative)

    def test_comments(self):
        pattern, negative = get_pattern_from_line(line='#env3')
        self.assertIsNone(pattern)
        pattern, negative = get_pattern_from_line(line='  #env3')
        self.assertIsNone(pattern)
        pattern, negative = get_pattern_from_line(line='\#env3')
        self.assertIsNotNone(pattern)


class GitIgnoreTestCase(unittest.TestCase):
    def test_ignore_lines(self):
        lines = ['abc/def', 'a/b/c', 'b']
        ignore = GitIgnore(lines)

        #  Paths which are targeted by the above 'lines'
        assert ignore.match('abc/def/child') is True, 'abc/def/child should match'
        assert ignore.match('a/b/c/d') is True, 'a/b/c/d should match'

        #  Paths which are not targeted by the above 'lines'
        assert ignore.match('abc') is False, 'abc should not match'
        assert ignore.match('def') is False, 'def should not match'
        assert ignore.match('bd') is False, 'bd should not match'

    def test_empty(self):
        ignore = GitIgnore([])

        assert ignore.match('a') is False, 'should not match any path'
        assert ignore.match('a/b') is False, 'should not match any path'
        assert ignore.match('.foobar') is False, 'should not match any path'

    def test_exclude_everything(self):
        ignore = GitIgnore([
            '# exclude everything except directory foo/bar',
            '/*',
            '!/foo',
            '/foo/*',
            '!/foo/bar'
        ])
        assert ignore.match('a') is True, 'a should match'
        assert ignore.match('foo/baz') is True, 'foo/baz should match'
        assert ignore.match('foo') is False, 'foo should not match'
        assert ignore.match('/foo/bar') is False, '/foo/bar should not match'

    def test_handle_spaces(self):
        ignore = GitIgnore([
            '#',
            '# A comment',
            '           ',
            '    # Another comment',
            '             ',
            '# Invalid Comment',
            'abc/def',
        ])

        self.assertEqual(1, len(ignore.items))
        assert ignore.match('abc/abc') is False, '/abc/abc should not match'
        assert ignore.match('abc/def') is True, '/abc/def should match'

    def test_handle_leading_slashes(self):
        ignore = GitIgnore([
            '/a/b/c',
            'd/e/f',
            '/g',
        ])

        self.assertEqual(3, len(ignore.items))
        assert ignore.match('a/b/c'), 'a/b/c should match'
        assert ignore.match('a/b/c/d'), 'a/b/c/d should match'
        assert ignore.match('d/e/f'), 'd/e/f should match'
        assert ignore.match('g'), 'g should match'

    def test_handle_leading_special_chars(self):
        ignore = GitIgnore([
            '# Comment',
            '\#file.txt',
            '\!file.txt',
            'file.txt',
        ])

        assert ignore.match('#file.txt'), '#file.txt should match'
        assert ignore.match('!file.txt'), '!file.txt should match'
        assert ignore.match('a/!file.txt'), 'a/!file.txt should match'
        assert ignore.match('file.txt'), 'file.txt should match'
        assert ignore.match('a/file.txt'), 'a/file.txt should match'
        assert not ignore.match('file2.txt'), 'file2.txt should not match'

    def test_handle_all_files_in_dir(self):
        ignore = GitIgnore(['Documentation/*.html'])

        assert ignore.match('Documentation/git.html'), 'Documentation/git.html should match'
        assert not ignore.match('Documentation/ppc/ppc.html'), 'Documentation/ppc/ppc.html should not match'
        assert ignore.match('tools/perf/Documentation/perf.html'), 'tools/perf/Documentation/perf.html should not match'

    def test_handle_double_star(self):
        ignore = GitIgnore(['**/foo', 'bar'])

        assert ignore.match('foo'), 'foo should match'
        assert ignore.match('baz/foo'), 'baz/foo should match'
        assert ignore.match('bar'), 'bar should match'
        assert ignore.match('baz/bar'), 'baz/bar should match'

    def test_handle_leading_slash_path(self):
        ignore = GitIgnore(['/*.c'])

        assert ignore.match('hello.c'), 'hello.c should match'
        assert not ignore.match('foo/hello.c'), 'foo/hello.c should not match'

    def test_nested_dot_files(self):
        ignore = GitIgnore([
            '**/external/**/*.md',
            '**/external/**/*.json',
            '**/external/**/*.gzip',
            '**/external/**/.*ignore',

            '**/external/foobar/*.css',
            '**/external/barfoo/less',
            '**/external/barfoo/scss',
        ])
        assert ignore.match('external/foobar/angular.foo.css'), 'external/foobar/angular.foo.css'
        assert ignore.match('external/barfoo/.gitignore'), 'external/barfoo/.gitignore'
        assert ignore.match('external/barfoo/.bower.json'), 'external/barfoo/.bower.json'

    def test_wild_card_files(self):
        ignore = GitIgnore(['*.swp', '/foo/*.wat', 'bar/*.txt'])

        assert ignore.match('yo.swp'), 'should ignore all swp files'
        assert ignore.match('something/else/but/it/hasyo.swp'), 'should ignore all swp files in other directories'

        assert ignore.match('foo/bar.wat'), 'should ignore all wat files in foo - nonpreceding /'
        assert ignore.match('/foo/something.wat'), 'should ignore all wat files in foo - preceding /'

        assert ignore.match('bar/something.txt'), 'should ignore all txt files in bar - nonpreceding /'
        assert ignore.match('/bar/somethingelse.txt'), 'should ignore all txt files in bar - preceding /'

        assert not ignore.match('something/not/infoo/wat.wat'), 'wat files should only be ignored in foo'
        assert not ignore.match('something/not/infoo/wat.txt'), 'txt files should only be ignored in bar'

    def test_preceding_slash(self):
        ignore = GitIgnore(['/foo', 'bar/'])

        assert ignore.match('foo/bar.wat'), 'should ignore all files in foo - nonpreceding /'
        assert ignore.match('/foo/something.txt'), 'should ignore all files in foo - preceding /'

        assert ignore.match('bar/something.txt'), 'should ignore all files in bar - nonpreceding /'
        assert ignore.match('/bar/somethingelse.go'), 'should ignore all files in bar - preceding /'
        assert ignore.match('/boo/something/bar/boo.txt'), 'should block all files if bar is a sub directory'

        assert not ignore.match(
            'something/foo/something.txt'), 'should only ignore top level foo directories- not nested'
