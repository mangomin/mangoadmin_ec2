from boto.ec2.connection import EC2Connection

class EC2Go(object):

    def __init__(self, access_key,
                       secret_key,
                       keyname,
                       **args):

        self.conn = EC2Connection(access_key,
                                  secret_key)
        self.vpc_id = None
        self.subnet_id = None
        self.keyname = keyname
        if 'vpc' in args:
            self.vpc_id = args['vpc']['vpc_id']
            self.subnet_id = args['vpc']['subnet_id']

    def run_instances(self, image_id, instance_type, min_count=1,
                      max_count=1, security_groups=None,
                      placement=None, user_data=None, placement_group=None):

        if self.subnet_id:
            sec_group_ids = self.get_securityids_from_names(security_groups)

            return self.conn.run_instances(image_id,
                                           instance_type=instance_type,
                                           min_count=min_count,
                                           max_count=max_count,
                                           key_name=self.keyname,
                                           security_group_ids=sec_group_ids,
                                           subnet_id=self.subnet_id,
                                           placement=placement,
                                           user_data=user_data,
                                           placement_group=placement_group)
        else:

            return self.conn.run_instances(image_id,
                                           instance_type=instance_type,
                                           min_count=min_count,
                                           max_count=max_count,
                                           key_name=key_name,
                                           security_groups=security_groups,
                                           placement=placement,
                                           user_data=user_data,
                                           placement_group=placement_group)

    def create_security_group(self, name, description, auth_ssh=False,
                     auth_group_traffic=False):
        """
        Create security group with name/description. auth_ssh=True
        will open port 22 to world (0.0.0.0/0). auth_group_traffic
        will allow all traffic between instances in the same security
        group
        """
        if not name:
            return None
        log.info("Creating security group %s..." % name)
        sg = self.conn.create_security_group(name, description, self.vpc_id)
        if auth_ssh:
            ssh_port = static.DEFAULT_SSH_PORT
            self.conn.authorize_security_group(group_id=sg.id,
                    ip_protocol='tcp', from_port=ssh_port, to_port=ssh_port,
                    cidr_ip=static.WORLD_CIDRIP)
        if auth_group_traffic:
            self.conn.authorize_security_group(group_id=sg.id,
                    ip_protocol='icmp', from_port=-1, to_port=-1,
                    cidr_ip=static.WORLD_CIDRIP)
            self.conn.authorize_security_group(group_id=sg.id,
                    ip_protocol='tcp', from_port=1, to_port=65535,
                    cidr_ip=static.WORLD_CIDRIP)
            self.conn.authorize_security_group(group_id=sg.id,
                    ip_protocol='udp', from_port=1, to_port=65535,
                    cidr_ip=static.WORLD_CIDRIP)
        return sg
