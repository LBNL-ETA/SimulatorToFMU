from pymodelica import compile_fmu

fmu_name = compile_fmu("{{model_name}}", "{{model_name}}.mo", 
                       version="{{fmi_version}}", target="{{fmi_api}}",
                       compiler_options={'extra_lib_dirs':["{{sim_lib_path}}"]})




