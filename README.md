# auto_ac_ansible

Auto AC... because the AC in my building isn't designed very well.

The AC unit in my apartment keeps the blower running even if the set temperature is reached, all it does is turns off the AC compressor. This has the effect of warming up the apartment by blowing non-cooled air along with evaporating all the humidity the AC took out of the air and adding it back to the apartment. 

Not the greatest level of control:
![image](https://user-images.githubusercontent.com/66385638/126082740-abe26536-7e84-422d-a00c-91164ac866e4.png)

Using two Pi Zero's, one as a temp sensor and one as a servo controller, the AC can be fully turned on and off based on more precise temperature readings. This also prevents the blower from running when the AC isn't on and cooling the apartment. Since there are two AC units in my apartment, multiple temperature sensors and controllers will be linked togheter to intellegently cool the apartment.

Future plans are to add a GUI front end to control the networked units and scheduling.

## Initial Setup

This project uses Ansible to push out necessary dependencies and configuring the services.

### Build Docker Container

1. Clone repo
2. In repo root, run ```docker build -t aac_container .```

### Set Credentials

The following variables will need to be set:

* ```ansible_user:``` - pi login name (pi default is `pi`)
* ```ansible_password:``` - pi password (pi default is `raspberry`)
* ```ansible_become_pass:``` - pi password (pi default is `raspberry`)

Files where variables reside:

* ```inventory\group_vars\all.yml```

Setting the variables in plaintext works but is obviously insecure. You can use [ansible-vault encrypt_string](https://docs.ansible.com/ansible/latest/user_guide/vault.html#use-encrypt-string-to-create-encrypted-variables-to-embed-in-yaml) to keep your secrets encrypted. Do not press enter after your password, press ctrl-d twice.

```bash
bash$ ./sre ansible-vault encrypt_string --ask-vault-pass
New Vault password:
Confirm New Vault password:
Reading plaintext input from stdin. (ctrl-d to end input)
yourpassword!vault |
          $ANSIBLE_VAULT;1.1;AES256
          35373765373164393437356235323037663263393032623961303333373263346437653832363938
          3433386662356666643232646361633763336435633366610a616534623063643832316563353134
          34313565383338313763656163623432663862303766643037373839383466383930356436373439
          6231643335633036660a373933373937613834333537643939323963303661353466646566613439
          3064
Encryption successful
```

The resulting variable will be set like so:

```yaml
ansible_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35373765373164393437356235323037663263393032623961303333373263346437653832363938
          3433386662356666643232646361633763336435633366610a616534623063643832316563353134
          34313565383338313763656163623432663862303766643037373839383466383930356436373439
          6231643335633036660a373933373937613834333537643939323963303661353466646566613439
          3064
ansible_become_pass: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35373765373164393437356235323037663263393032623961303333373263346437653832363938
          3433386662356666643232646361633763336435633366610a616534623063643832316563353134
          34313565383338313763656163623432663862303766643037373839383466383930356436373439
          6231643335633036660a373933373937613834333537643939323963303661353466646566613439
          3064
```
