# auto_ac_ansible

Auto AC... because the AC in my building isn't designed very well.

The AC unit in my apartment keeps the blower running even if the set temperature is reached, it only turns off the AC compressor when the set temperature is reached. This has the effect of warming up the apartment by blowing non-cooled air along with evaporating all the humidity the AC took out of the air and adding it back to the apartment.

Not the greatest level of control:
![image](https://user-images.githubusercontent.com/66385638/126082740-abe26536-7e84-422d-a00c-91164ac866e4.png)

#### Why not just use a [smart outlet](https://www.amazon.com/Amazon-smart-plug-works-with-Alexa/dp/B089DR29T6) to control the AC, there are plenty of thermostat apps that work with smart outlets?

Unfortunately the AC units run on a [20 AMP plug](https://www.google.com/search?q=20+amp+plug&rlz=1C1GCEU_enUS925US925&source=lnms&tbm=isch&sa=X&ved=2ahUKEwif39alju7xAhWEGFkFHQ7ZAcQQ_AUoAXoECAEQAw&biw=2560&bih=1329) and there are no 20 AMP smart outlets. I could do something similar with a [relay](https://alselectro.wordpress.com/2018/09/26/raspberry-pi-all-about-controlling-relay-boards-for-home-automation/) controlled by a Pi but in case or error, I'd rather deal with the AC being on for too long or not at all versus a possible electrical fire.

Using two Pi Zero's, one as a temp sensor and one as a servo controller, the AC can be fully turned on and off based on more precise temperature readings. This also prevents the blower from running when the AC isn't on and cooling the apartment. Since there are two AC units in my apartment, multiple temperature sensors and controllers will be linked togheter to intellegently cool the apartment.

Future plans are to add a GUI front end to control the networked units and scheduling.

### Hardware Used:

* [Pi Zero W](https://www.amazon.com/Raspberry-Pi-Zero-Wireless-model/dp/B06XFZC3BX/ref=sr_1_5?dchild=1&keywords=pi+zero&qid=1626648508&sr=8-5)
* [SparkFun Servo pHAT for Raspberry Pi](https://www.sparkfun.com/products/15316)
* [DHT22/AM2302 Digital Temperature Humidity Sensor Module](https://www.amazon.com/gp/product/B073F472JL/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
* [D Shaft Coupling](https://www.amazon.com/gp/product/B07R78458M/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
* [Servo](https://www.sparkfun.com/products/11965)



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
