## Product Vision
Set of python scripts that define a ModelDriver class which is capable of execute a "model" in a given dataset, and get results according to configuration.
In order to develop this "model" or set of filters, and attributes the class is prepared to load the functions in 2 different ways: from functiones defined in code during the script execution or getting them from a registry. The workflow for a given developer using this tool should be the following:
1. Get data.
2. Define filters and attributes using that data.
3. Define output attributes to calculate.
4. Get required input fields, dependencies and order of execution of calculations.
5. Set dictionary master configuration that specifies output attributes and scores, order of execution of calculation, groupby key, model name, model seq in case other model will use the output as input.
6. Execute using master configuration, and produce intermediate files based on configuration(client_name and model_name should be replaced with corresponding values)
   6.1. write preprocess file, or input after preprocessing on data_management/client_name/model_name/01_preprocess/
   6.2. write filters file, or preprocess file with filters on data_management/client_name/model_name/02_features/
   6.2. write attributes file, or file with attributes by groupby key on data_management/client_name/model_name/03_attributes/
   6.2. write output file, or file with output attributes by groupby key on data_management/client_name/model_name/04_output/ 
7. Once results look good, developer should be able to register the created filters and attributes, all in the same folder.
8. And them execute the model again but loading the filters and attributes from this folder instead of the code. The idea is that the features(filters and attributes) are stores or registered in plain code. These features should be self contined so they ca be taken to be executed by other models too.

In order to get a better idea of this approach do an analysis on the architecture, functions and data flow in the following notebooks, refine it and lets iterateon it asking me questions in order to reach an understanding about what structure to follow:
- "C:\Projects\play\khujta_ai_business\reference\personalbrownbull-vecmodels-08af286a6a71\personalbrownbull-vecmodels-08af286a6a71\prpf1_cp\A00_prpf1_pp_cp.ipynb"
- "C:\Projects\play\khujta_ai_business\reference\personalbrownbull-vecmodels-08af286a6a71\personalbrownbull-vecmodels-08af286a6a71\prpf1_ct\A00_prpf1_pt_2_ct.ipynb"
- "C:\Projects\play\khujta_ai_business\reference\personalbrownbull-vecmodels-08af286a6a71\personalbrownbull-vecmodels-08af286a6a71\prpf1_pa\A00_prpf1_pa.ipynb"
- "C:\Projects\play\khujta_ai_business\reference\personalbrownbull-vecmodels-08af286a6a71\personalbrownbull-vecmodels-08af286a6a71\prpf1_pp\A00_prpf1_pp.ipynb"
- "C:\Projects\play\khujta_ai_business\reference\personalbrownbull-vecmodels-08af286a6a71\personalbrownbull-vecmodels-08af286a6a71\prpf1_pt\A00_prpf1_pt.ipynb"

## Observations from last feature engine refactoring
### Missing
- No place to define a subset of attributes to execute once they are defined, this should be dynamic, so if I defined attributes a,b,c which required input a1,a2,b1,c1 and then ask for only attributes a,c in output, then the input required should be a1,a2,c1. this way different configurations could required different input based on desired calculations.

### Overcomplicated
- Features seemed overly complicated coded, check on example notebooks.