

# ---- LOGS

save_logs_backup: 
	mkdir -p backup_results_GCP
	make logbruh | cat - dump_temp/meta_data_for_run.out > backup_results_GCP/logs_`date +"%Y%m%d_%H%M%S"`.txt

make meta_data_for_backup: 
	cat hpl-mpi.yaml HPL.dat > dump_temp/meta_data_for_run.out


# -----

logbruh: 
	kubectl logs pod/`kubectl get pods | grep hpl-mpi-launcher | awk '{print $$1}'`

# run: 
# 	kubectl delete configmap config 
# 	kubectl apply 

delete: 
	make save_logs_backup
	kubectl delete configmap/config	--ignore-not-found
	kubectl delete mpijob/hpl-mpi	--ignore-not-found

create: 
	python3 check_args.py
	kubectl create configmap config --from-file HPL.dat	
	kubectl apply -f hpl-mpi.yaml
	make meta_data_for_backup	

all: 
	clear
	make delete	--keep-going
	make create	--keep-going
	make spectate


mpiapply: 
	kubectl apply -f /home/rohanjain_durham/rohan-jain/mpi-operator/deploy/v2beta1/mpi-operator.yaml


spectate:
	watch -n 5 'kubectl get pods; echo ""; kubectl top node'


pyCheckBruh: 
	watch -n 5 python3 show_results.py


# bruh: 
# 	echo pseto
# 	echo "hell"

