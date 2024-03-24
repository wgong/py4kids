
https://supabase.com/docs/guides/cli/local-development

```
cd ~/projects/wgong/supabase
mkdir zapp
cd zapp
git init
git config --global init.defaultBranch main
git branch -m main
supabase init
supabase start

Started supabase local development setup.

         API URL: http://127.0.0.1:54321
     GraphQL URL: http://127.0.0.1:54321/graphql/v1
          DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres
      Studio URL: http://127.0.0.1:54323
    Inbucket URL: http://127.0.0.1:54324
      JWT secret: super-secret-jwt-token-with-at-least-32-characters-long
        anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

supabase stop               #  stop all services without resetting your local database
supabase stop --no-backup   # stop all services and reset your local database.
```

https://gcore.com/learning/how-to-install-pgadmin4-on-ubuntu/

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql
curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add

sudo apt install pgadmin4-desktop

The following NEW packages will be installed:
  pgadmin4-desktop pgadmin4-server
```

?? don't know where pgadmin4-desktop is installed

supabase migration new create_employees_table

supabase db reset

verify table `employees` is created
- use supabase dashboard = http://localhost:54323/project/default/database/tables
- use dbeaver client

supabase migration new add_department_to_employees_table

use the seed script in `supabase/seed.sql` to add data


~/projects/wgong/supabase/zapp$ supabase stop
Stopped supabase local development setup.
Local data are backed up to docker volume. Use docker to show them: docker volume ls --filter label=com.supabase.cli.project=zapp

