from flask import Flask, render_template
import yaml


app = Flask(__name__)


def connect_to_aws(config)
    if 'profile' in config:
        session_params = dict(profile_name=config['profile'])
    if 'region' in config;
        params = dict(region_name = config['region'])
    return boto3.session.Session(**session_params).client('ec2', **params)


def get_ami_data(conn, config, ami_id):
    ami = conn.describe_images(dict(Filters=list(dict(Key='image-id', Value=ami_id))))['Images']
    tags = [(item['Name'],item['Value']) for item in ami['Tags']]
    results = dict(Name=ami.tags['Name'], tags=ami.tags)
    return results


def get_instance_data(conn, config, instance)
    tags = [(item['Name'],item['Value']) for item in instance['Tags']]
    instance = dict(tags=tags, name=tags['Name'], ami=get_ami_data(conn, config, instance['ImageId']))
    return instance


def get_environment_details(config):
    conn = connect_to_aws(config)
    results = OrderedDict()
    for environment in config['environments']:
        results[environment] = OrderedDict()
        for applications in config['applications']:
            filters=list(dict(Name='tag:%s' % config['tag_environment'], Value=environment),
                         dict(Name='tag:%s' % config['tag_application'], Value=application),
                         dict(Name='instance-state-name', Value='running'))
            instances = conn.describe_instances(Filters=filters)['Reservations']['Instances']
            results[environment][application] = [instance_data(conn, config, instance) for instance in instances]
    return results


@app.route('/')
def dashboard():
    with open(CONFIG_FILE) as config_file:
        config = yaml.load(config_file)
    data = get_environment_details(config)
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run()
