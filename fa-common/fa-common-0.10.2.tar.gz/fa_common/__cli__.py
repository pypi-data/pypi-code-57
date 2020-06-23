# import click
# import sys
# from loguru import logger
# from fa_common

# @click.group()
# @logger.catch
# def cli():
#     logger.remove()

#     logger.add(
#         sys.stdout,
#         enqueue=True,
#         level="DEBUG",
#         format="<green>{time:HH:mm:ss}</green> | <cyan>{process}</cyan> | <level>{message}</level>",
#     )


# @cli.command()
# @click.argument("job_id", type=str)
# @click.argument("filter_file_path", type=click.Path(exists=True))
# @click.option(
#     "--from", "-f", "from_", default="From", help="Filter Range From Column", type=str
# )
# @click.option("--to", "-t", default="To", help="Filter Range To Column", type=str)
# @click.option("--column", "-c", default="Depth", help="Data Filter Column", type=str)
# @click.option(
#     "--output", "-o", default="output.xlsx", help="File to output to", type=click.Path()
# )
# def job(data_file_path, filter_file_path, from_, to, column, output):
#     logger.debug("Filtering data from {} by range", data_file_path)
#     logger.debug("Filter File {}", filter_file_path)
#     logger.debug("Filter Range Columns From: {} To: {}", from_, to)
#     logger.debug("Data File Filter Column: {}", column)

#     filter_data_by_ranges_from_file(
#         data_file_path, filter_file_path, from_, to, column, output
#     )
#     logger.debug("Outputted to: {}", output)


# if __name__ == "__main__":
#     cli()
