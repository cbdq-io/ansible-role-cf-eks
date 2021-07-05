all:
	molecule lint

clean:
	molecule destroy

deploy:
	ansible-playbook -i inventories/CBDQ/aws/eu-west-2/production.yml site.yml

remove:
	ansible-playbook -i inventories/CBDQ/aws/eu-west-2/production.yml site.yml -e cf_eks_state=absent
