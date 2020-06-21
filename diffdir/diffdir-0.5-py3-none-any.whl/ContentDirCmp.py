import os
from path import Path
from filecmp import dircmp, cmpfiles


class ContentDirCmp(dircmp):
    def my_phase3(self):
        self.same_files, self.diff_files, self.funny_files = cmpfiles(
            self.left,
            self.right,
            self.common_files,
            shallow=False,  # shallow = False to make sure we will check file contents
        )

    def my_phase4(self):
        self.subdirs = {}
        for x in self.common_dirs:
            a_x = os.path.join(self.left, x)
            b_x = os.path.join(self.right, x)
            self.subdirs[x] = ContentDirCmp(a_x, b_x, self.ignore, self.hide)

    def get_diff_info(self):
        common_head = []
        for part_a, part_b in zip(
            Path(self.left).splitall()[::-1], Path(self.right).splitall()[::-1]
        ):
            if part_a != part_b:
                break
            common_head.append(part_a)
        if common_head:
            common_head = os.path.join(*common_head[::-1])
        else:
            common_head = ""
        file_lists = [
            self.left_only,
            self.right_only,
            self.diff_files,
            self.funny_files,
        ]
        ret = [None for _ in range(len(file_lists))]
        heads = [self.left, self.right, common_head, common_head]
        for i in range(len(ret)):
            if heads[i]:
                ret[i] = (f"{heads[i]}/{item}" for item in file_lists[i])  # generator
            else:
                ret[i] = (f"{item}" for item in file_lists[i])  # generator
        return ret  # left_only, right_only, diff_files, funny_files

    methodmap = dict(
        subdirs=my_phase4,
        same_files=my_phase3,
        diff_files=my_phase3,
        funny_files=my_phase3,
        common_dirs=dircmp.phase2,
        common_files=dircmp.phase2,
        common_funny=dircmp.phase2,
        common=dircmp.phase1,
        left_only=dircmp.phase1,
        right_only=dircmp.phase1,
        left_list=dircmp.phase0,
        right_list=dircmp.phase0,
    )

    def work(self):
        yield self.get_diff_info()
        for sd in self.subdirs.values():
            yield from sd.work()
