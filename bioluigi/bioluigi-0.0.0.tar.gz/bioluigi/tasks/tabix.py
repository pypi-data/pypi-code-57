from bioluigi.scheduled_external_program import ScheduledExternalProgramTask
import luigi

class Index(ScheduledExternalProgramTask):
    """Index a tabular format (VCF, TSV, etc.) using tabix utility"""
    input_file = luigi.Parameter()

    preset = luigi.ChoiceParameter(choices=['gff', 'bed', 'sam', 'vcf', 'psltbl'], positional=False)

    sequence_column = luigi.IntParameter()
    begin_column = luigi.IntParameter()
    end_column = luigi.IntParameter()
    skip_lines = luigi.IntParameter()
    comment_symbol = luigi.Parameter()

    def program_args(self):
        return ['tabix', '-p', self.preset, self.input_file]

    def output(self):
        return luigi.LocalTarget(self.input_file + '.tbi')
