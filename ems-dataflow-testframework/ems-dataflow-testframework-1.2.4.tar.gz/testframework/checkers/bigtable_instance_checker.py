import logging

from google.cloud.bigtable.column_family import MaxAgeGCRule, GCRuleUnion


class BigTableInstanceChecker():
    def __init__(self, bt_instance, expected_tables_with_column_families_and_ttls):
        self.__bt_instance = bt_instance
        logging.info("Instance is: {}".format(self.__bt_instance.instance_id))
        self.__expected_tables_with_column_families_and_ttls = expected_tables_with_column_families_and_ttls

    def check_tables(self):
        existing_tables = self.__bt_instance.list_tables()
        set_of_existing_bigtable_table_names = \
            set([self.__get_short_table_name(table) for table in existing_tables])
        logging.info("Current tables in bigtable [{} pieces]: {}".format(
            len(set_of_existing_bigtable_table_names),
            set_of_existing_bigtable_table_names))

        if not set(self.__expected_tables_with_column_families_and_ttls.keys()).issubset(set_of_existing_bigtable_table_names):
            logging.info(
                "Missing tables are: {}"
                    .format([ds for ds in set(self.__expected_tables_with_column_families_and_ttls
                                              .keys()).difference(set_of_existing_bigtable_table_names)]))
            return False

        is_valid = True
        for table in existing_tables:
            table_short_name = self.__get_short_table_name(table)
            if table_short_name in self.__expected_tables_with_column_families_and_ttls.keys():
                expected_cf = self.__expected_tables_with_column_families_and_ttls[table_short_name][0]
                expected_ttl = self.__expected_tables_with_column_families_and_ttls[table_short_name][1]
                if not self.__check_column_family(table, expected_cf) \
                        or not self.__check_column_family_ttl(table, expected_cf, expected_ttl):
                    is_valid = False

        return is_valid

    def __check_column_family(self, bigtable_table, expected_cf):
        if expected_cf in bigtable_table.list_column_families().keys():
            return True
        logging.info("Could not find expected column family ({}) for table {}"
                     .format(expected_cf,
                             self.__get_short_table_name(bigtable_table)))

        return False

    def __check_column_family_ttl(self, bigtable_table, expected_cf, expected_ttl):
        if expected_ttl is None:
            return True

        short_table_name = self.__get_short_table_name(bigtable_table)
        cf_gc_rules = bigtable_table.list_column_families()[expected_cf].gc_rule
        if isinstance(cf_gc_rules, GCRuleUnion):
            max_age_rules_list = [rule for rule in cf_gc_rules.rules if isinstance(rule, MaxAgeGCRule)]
        elif isinstance(cf_gc_rules, MaxAgeGCRule):
            max_age_rules_list = [cf_gc_rules]
        else:
            return False

        assert len(max_age_rules_list) == 1, "No single max age rule for ({}:{}) column family!" \
            .format(short_table_name, expected_cf)

        max_age_total_seconds = max_age_rules_list[0].max_age.total_seconds()
        assert expected_ttl == max_age_total_seconds, \
            "TTL is wrong on table ({}). {} != {}".format(short_table_name,
                                                          expected_ttl,
                                                          max_age_total_seconds)
        return True

    def __get_short_table_name(self, bigtable_table):
        return bigtable_table.name.split('/')[-1]
