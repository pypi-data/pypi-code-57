from willowlabs.company_information.client import CompanyInformationClient
import datetime as dt
import csv

org_list = [
    917813752,
    917813817,
    917813825,
    917813833,
    917813876,
    917813884,
    917813906,
    917813930,
    917814015,
    917814090,
    917814120,
    917814201,
    917814333,
    917814597,
    917814694,
    917814708,
    917814783,
    917814880,
    917814899,
    917814929,
    917815038,
    917815186,
    917815283,
    917815429,
    917815461,
    917815593,
    917815704,
    917815771,
    917815801,
    917815860,
    917815909,
    917816085,
    917816212,
    917816328,
    917816379,
    917816387,
    917816425,
    917816581,
    917816638,
    917816662,
    917816697,
    917816727,
    917816808,
    917816816,
    917816891,
    917816980,
    917817014,
    917817448,
    917817464,
    917817561,
    917817588,
    917817936,
    917818061,
    917818088,
    917818096,
    917818118,
    917818355,
    917818843,
    917818851,
    917818908,
    917818983,
    917819009,
    917819041,
    917819068,
    917819084,
    917819149,
    917819238,
    917819262,
]


client = CompanyInformationClient("C:\\Users\\Sven\\projects\\client_config.yaml")


error_list = []

for org in org_list:
    result = client.get_company_roles(org, query_date=dt.datetime.today())
    print(result)
    error_list.append([org, result.server_error])


with open("../testing_out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(error_list)
