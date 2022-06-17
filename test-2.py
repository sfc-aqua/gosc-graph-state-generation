import two_tile_patch_ver as twotile

result=[]
num_op=0
for i in range(50):
    num_step_scheduled, num_stablizers=twotile.main()
    if num_step_scheduled< num_stablizers:
        print("After scheduling: "+str(num_step_scheduled)+ " Before scheduling: "+ str(num_stablizers))
        num_op+=1
    result.append([num_step_scheduled, num_stablizers])
print("Percentage of optimized after scheduing= "+str(num_op/50))