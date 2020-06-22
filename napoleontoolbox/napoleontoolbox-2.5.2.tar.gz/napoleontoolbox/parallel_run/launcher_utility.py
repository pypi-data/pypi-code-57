def get_database_name(user, frequence, underlying, algo, starting_date, running_date, db_path_suffix):
    return  user + '_' + frequence + '_' + underlying + '_' + algo + '_'+ starting_date.strftime(
        '%d_%b_%Y') + '_' + running_date.strftime('%d_%b_%Y') + db_path_suffix