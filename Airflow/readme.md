## Install Airflow on Windows using WSL

Open ~./bashrc and add this command

    export PATH="/home/fontlil/.local/bin:$PATH"
    AIRFLOW_HOME="/mnt/[airflow_directory]"


`source ~./bashrc`

Set Up the Virtual Environment

`pip install virtualenv `

`virtualenv airflow_env `

`source airflow_env/bin/activate`

`cd $AIRFLOW_HOME`

Install Apache Airflow

`pip install "apache-airflow==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.x.txt"`

`airflow db migrate` 

Create an Airflow User

`airflow users create -u admin -p admin -r Admin -e "[email]" -f admin -l admin`

`airflow users list`

Run the Webserver

`airflow scheduler`

Launch another terminal, active airflow virtual environment and cd to $AIRFLOW_HOME

`airflow webserver` | `airflow webserver –port <port number>`

