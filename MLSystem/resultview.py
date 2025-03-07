import pandas as pd
import similarity as sm
import matplotlib.pyplot as plt

def tenant_visualization(similarity_matrix, requested_tenants):
    #TODO VIEW COMPATIBILITY BETWEEN REQUESTED TENANTS
    print(f"The options for visualizatio are:\n"+
          "1.Compatibility for each tenants with requested ones\n"+
          "2.Mean compatibility for each tenant\n"+
          "3.Most compatible tenant for the requested ones\n"+
          "4.Obtain registers from most compatible tenants\n")
    option = int(input("What option are u choosing: "))
    tenant_lines = similarity_matrix[requested_tenants].mean()
    match(option):

        case 1:
            tenant_lines.head(5)
            print(f"Compatibility for each tenants with requested ones \n{tenant_lines}")

        case 2:
            mean_compatibility = tenant_lines.mean(axis = 0)
            print(f"Mean compatibility for each tenant:\n {mean_compatibility} ")

        case 3:
            most_compatible = tenant_lines.sort_values(ascending = False)
            print(f"Max compatibility for each tenant:\n {most_compatible} ")
        
        case 4:
            most_compatible = tenant_lines.sort_values(ascending = False)
            most_compatible = dataframe.loc[requested_tenants]
            print(f"Most compatible tenants registers\n {most_compatible}")

def view_kmeans_results(results,cluster_center): 
    # TODO FUNCTION TO VIEW KMEANS RESULTS
    print(f"Starting kmeans viewing \n Cluster length: {results.shape}")
    plt.scatter(results,results)
    plt.show()

def tenant_inference(similarity_matrix, requested_tenants,dataframe):
    #TODO THIS FUNCTION IS THE ONE USED DURING INFERENCE TIME THE MODEL WILL CALCULATE THE 4 TENANTS WITH THE HIGHER COMPATIBILITY
    similarity_tenant = similarity_matrix[requested_tenants].head(4).sort_values(ascending = False)
    final_tenants = similarity_tenant.index
    tenant_list = []

    for tenant in final_tenants:
        similarity = similarity_matrix[requested_tenants][tenant]
        tenant_tuple = (dataframe.loc[tenant, ['Names', 'Age','Smoking','Email']], float(similarity))
        tenant_list.append(tenant_tuple)

    #TODO WE CAN ACCESS THE INFO BY DOING tenant_list[index]['Column_Name]'
    #for tenant in tenant_list:
        #print(f"I will present the names of the tenants with the higher similarity: \n {tenant[0]['Names']}")
    return tenant_list

def algo_start(id):

    dataframe, original_dataframe = sm.data_preparing()
    #sm.data_checking(dataframe)
    similarity_matrix = sm.encoder_matrix(dataframe, min_range = 0, max_range=100)
    tenant_list = tenant_inference(similarity_matrix, id,original_dataframe)
    return tenant_list

    #tenant_visualization(similarity_matrix, [20,40,50,18,15])
