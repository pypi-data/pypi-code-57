from devyzer.commands.utiles import run_command
from devyzer.utils.cli import print_with_color
from devyzer.commands.__init__ import Command


# php artisan make:model modelName -m
class MakeModelCommand(Command):
    def name(self):
        return "artisan_make-model"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:model '
        if 'model_name' in args:
            command += args['model_name'] + ' '
        else:
            print_with_color("I need the name of the model..", '\033[91m')
            return False

        if 'with_resource' in args and args['with_resource'] is True:
            command += '--resource '
        if 'with_migration' in args and args['with_migration'] is True:
            command += '--migration '
        if 'with_controller' in args and args['with_controller'] is True:
            command += '--controller'
        return run_command(command)


# php artisan make:controller controllerName --resource
class MakeControllerCommand(Command):
    def name(self):
        return "artisan_make-controller"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:controller '
        if 'controller_name' in args:
            command += args['controller_name'] + ' '
        else:
            print_with_color("I need the name of the controller..", '\033[91m')
            return False
        if 'with_resource' in args and args['with_resource'] is True:
            command += '--resource '
        if 'with_model' in args:
            command += '--model=' + args['with_model'] + ' '
        if 'with_parent' in args:
            command += '--parent=' + args['with_parent']
        return run_command(command)


# php artisan make:migration migrationName
class MakeMigrationCommand(Command):
    def name(self):
        return "artisan_make-migration"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:migration '
        if 'migration_name' in args:
            command += args['migration_name'] + ' '
        else:
            print_with_color("I need the name of the migration..", '\033[91m')
            return False
        if 'with_table' in args:
            command += '--create=' + args['with_table'] + ' '
        if 'migrate_table' in args:
            command += '--table=' + args['migrate_table'] + ' '
        if 'location' in args:
            command += '--path=' + args['location']
        return run_command(command)


# php artisan make:seeder seeder_name
class MakeSeederCommand(Command):
    def name(self):
        return "artisan_make-seeder"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:seeder '
        if 'seeder_name' in args:
            command += args['seeder_name']
            return run_command(command)
        else:
            print_with_color("I need the name of the seeder..", '\033[91m')
            return False


# php artisan make:request request_name
class MakeRequestCommand(Command):
    def name(self):
        return "artisan_make-request"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:request '
        if 'request_name' in args:
            command += args['request_name']
            return run_command(command)
        else:
            print_with_color("I need the name of the request..", '\033[91m')
            return False


# php artisan make:middleware middlewareName
class MakeMiddlewareCommand(Command):
    def name(self):
        return "artisan_make-middleware"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:middleware '
        if 'middleware_name' in args:
            command += args['middleware_name']
            return run_command(command)
        else:
            print_with_color("I need the name of the middleware..", '\033[91m')
            return False


# php artisan make:policy policyName
class MakePolicyCommand(Command):
    def name(self):
        return "artisan_make-policy"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:policy '
        if 'policy_name' in args:
            command += args['policy_name'] + ' '
        else:
            print_with_color("I need the name of the policy..", '\033[91m')
            return False

        if 'with_model' in args:
            command += '--model=' + args['with_model']
        return run_command(command)


# php artisan make:auth --views --force
class MakeAuthCommand(Command):
    def name(self):
        return "artisan_make-auth"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:auth'
        if 'only_auth_views' in args and args['only_auth_views'] is True:
            command += ' --views'
        if 'overwrite_views' in args and args['overwrite_views'] is True:
            command += ' --force'
        return run_command(command)


# php artisan make:Command commandName --command=terminalName
class MakeComCommand(Command):
    def name(self):
        return "artisan_make-command"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:command '
        if 'command_name' in args:
            command += args['command_name'] + ' '
        else:
            print_with_color("I need the name of the command..", '\033[91m')
            return False

        if 'with_command' in args:
            command += args['with_command']

        return run_command(command)


# php artisan make:Event eventName
class MakeEventCommand(Command):
    def name(self):
        return "artisan_make-event"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:event '
        if 'event_name' in args:
            command += args['event_name']
        else:
            print_with_color("I need the name of the event..", '\033[91m')
            return False
        return run_command(command)


# php artisan make:Job jobName
class MakeJobCommand(Command):
    def name(self):
        return "artisan_make-job"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:job '
        if 'job_name' in args:
            command += args['job_name'] + ' '
        else:
            print_with_color("I need the name of the job..", '\033[91m')
            return False
        if 'with_sync' in args and args['with_sync'] is True:
            command += '--sync'

        return run_command(command)


# php artisan make:listener listenerName
class MakeListenerCommand(Command):
    def name(self):
        return "artisan_make-listener"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:listener '
        if 'listener_name' in args:
            command += args['listener_name'] + ' '
        else:
            print_with_color("I need the name of the listener..", '\033[91m')
            return False

        if 'with_event' in args:
            command += '--event=' + args['with_event'] + ' '
        if 'should_be_queued' in args and args['should_be_queued'] is True:
            command += '--queued'

        return run_command(command)


# php artisan make:mail mailName --markdown
class MakeMailCommand(Command):
    def name(self):
        return "artisan_make-mail"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:mail '
        if 'mail_name' in args:
            command += args['mail_name']
        else:
            print_with_color("I need the name of the mail..", '\033[91m')
            return False

        if 'with_markdown' in args and args['with_markdown'] is True:
            command += ' --markdown'

        return run_command(command)


# php artisan make:notification notificationName --markdown
class MakeNotificationCommand(Command):
    def name(self):
        return "artisan_make-notification"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:notification '
        if 'notification_name' in args:
            command += args['notification_name']
        else:
            print_with_color("I need the name of the notification..", '\033[91m')
            return False

        if 'with_markdown' in args and args['with_markdown'] is True:
            command += ' --markdown'

        return run_command(command)


# php artisan make:provider providerName
class MakeProviderCommand(Command):
    def name(self):
        return "artisan_make-provider"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:provider '
        if 'provider_name' in args:
            command += args['provider_name']
            return run_command(command)
        else:
            print_with_color("I need the name of the provider..", '\033[91m')
            return False


# php artisan make:test testName --unit
class MakeTestCommand(Command):
    def name(self):
        return "artisan_make-test"

    def run(self, args, sio, project_configuration):
        command = 'php artisan make:test '
        if 'test_name' in args:
            command += args['test_name']
        else:
            print_with_color("I need the name of the test..", '\033[91m')
            return False

        if 'with_unit' in args and args['with_unit'] is True:
            command += ' --unit'

        return run_command(command)


# php artisan env
class DisplayEnvCommand(Command):
    def name(self):
        return "artisan_env"

    def run(self, args, sio, project_configuration):
        command = 'php artisan env'
        return run_command(command)


# php artisan app:name appName
class ChangeAppNameCommand(Command):
    def name(self):
        return "artisan_change-app-name"

    def run(self, args, sio, project_configuration):
        command = 'php artisan app:name '
        if 'app_name' in args:
            command += args['app_name']
            return run_command(command)
        else:
            print_with_color("I need the name of the application..", '\033[91m')
            return False


# php artisan --version
class PrintVersionCommand(Command):
    def name(self):
        return "artisan_print-version"

    def run(self, args, sio, project_configuration):
        command = 'php artisan --version'
        return run_command(command)


# php artisan down
class GoToMaintenanceModeCommand(Command):
    def name(self):
        return "artisan_go-to-maintenance-mode"

    def run(self, args, sio, project_configuration):
        command = 'php artisan down'
        return run_command(command)


# php artisan up
class OutOfMaintenanceModeCommand(Command):
    def name(self):
        return "artisan_out-of-maintenance-mode"

    def run(self, args, sio, project_configuration):
        command = 'php artisan up'
        return run_command(command)


# php artisan serve --host=[with_host] --port=[with_port]
class ServeCommand(Command):
    def name(self):
        return "artisan_serve"

    def run(self, args, sio, project_configuration):
        command = 'php artisan serve '
        if 'with_host' in args:
            command += '--host=' + args['with_host']
        if 'with_port' in args:
            command += '--port=' + args['with_port']
        return run_command(command)


# php artisan list
class ListCommand(Command):
    def name(self):
        return "artisan_route-list"

    def run(self, args, sio, project_configuration):
        command = 'php artisan list'
        return run_command(command)


# php artisan migrate --force --path=[location] --pretend --seed --database=[with_database]
class MigrateCommand(Command):
    def name(self):
        return "artisan_migrate"

    def run(self, args, sio, project_configuration):
        command = 'php artisan migrate'
        if 'with_force' in args and args['with_force'] is True:
            command += ' --force'
        if 'location' in args:
            command += ' --path=' + args['location']
        if 'with_seed' in args and args['with_seed'] is True:
            command += ' --seed'
        if 'with_pretend' in args and args['with_pretend'] is True:
            command += ' --pretend'
        if 'with_database' in args:
            command += ' --database=' + args['with_database']

        return run_command(command)


# php artisan migrate:install --database=[with_database]
class MigrateInstallCommand(Command):
    def name(self):
        return "artisan_migrate-install"

    def run(self, args, sio, project_configuration):
        command = 'php artisan migrate:install '
        if 'with_database' in args:
            command += ' --database=' + args['with_database']

        return run_command(command)


# php artisan migrate:refresh --database=[with_database] --path=[location] --force --seed --seeder=[with_seeder]
class MigrateRefreshCommand(Command):
    def name(self):
        return "artisan_migrate-refresh"

    def run(self, args, sio, project_configuration):
        command = 'php artisan migrate:refresh '
        if 'with_seeder' in args:
            command += ' --seeder=' + args['with_seeder']
        if 'with_force' in args and args['with_force'] is True:
            command += ' --force'
        if 'location' in args:
            command += ' --path=' + args['location']
        if 'with_seed' in args and args['with_seed'] is True:
            command += ' --seed'
        if 'with_pretend' in args and args['with_pretend'] is True:
            command += ' --pretend'
        if 'with_database' in args:
            command += ' --database=' + args['with_database']

        return run_command(command)


# php artisan migrate:reset --database=[with_database] --force  --pretend
class MigrateResetCommand(Command):
    def name(self):
        return "artisan_migrate-reset"

    def run(self, args, sio, project_configuration):
        command = 'php artisan migrate:reset '
        if 'with_force' in args and args['with_force'] is True:
            command += ' --force'
        if 'with_pretend' in args and args['with_pretend'] is True:
            command += ' --pretend'
        if 'with_database' in args:
            command += ' --database=' + args['with_database']

        return run_command(command)


# php artisan migrate:rollback --database=[with_database] --pretend --step=[with_step]
class MigrateRollbackCommand(Command):
    def name(self):
        return "artisan_migrate-rollback"

    def run(self, args, sio, project_configuration):
        command = 'php artisan migrate:rollback '
        if 'with_step' in args:
            command += ' --step=' + args['with_step']
        if 'with_pretend' in args and args['with_pretend'] is True:
            command += ' --pretend'
        if 'with_database' in args:
            command += ' --database=' + args['with_database']

        return run_command(command)


# php artisan cache:clear
class ClearCacheCommand(Command):
    def name(self):
        return "artisan_cache-clear"

    def run(self, args, sio, project_configuration):
        command = 'php artisan cache:clear'
        return run_command(command)


# php artisan db:seed --database=[with_database] --force --seeder=[with_seeder]
class DBSeedCommand(Command):
    def name(self):
        return "artisan_db-seed"

    def run(self, args, sio, project_configuration):
        command = 'php artisan db:seed'
        if 'with_seeder' in args:
            command += ' --seeder=' + args['with_seeder']
        if 'with_force' in args and args['with_force'] is True:
            command += ' --force'
        if 'with_database' in args:
            command += ' --database=' + args['with_database']

        return run_command(command)


# php artisan dump-autoload
class DumpAutoloadCommand(Command):
    def name(self):
        return "artisan_cache-clear"

    def run(self, args, sio, project_configuration):
        command = 'php artisan dump-autoload'
        return run_command(command)


# php artisan key:generate --show
class KeyGenerateCommand(Command):
    def name(self):
        return "artisan_key-generate"

    def run(self, args, sio, project_configuration):
        command = 'php artisan key:generate'
        if 'with_show' in args and args['with_show'] is True:
            command += ' --show'
        return run_command(command)
