json_to_df <- function(output_list, model_name) {
  values = names(output_list)
  df_full = data.frame("model" = c(model_name))
  for (i in 1:length(output_list)) {
    if (typeof(output_list[[i]]) == "list") {
      if (values[i] == "total_process_emissions_kg_per_kg_h2") {
        if(length(output_list[[i]]) > 0) {
          columns = data.frame("CO2_process_emissions_kg_per_kg_h2" = c(output_list[[i]]$CO2), 
                               "CH4_process_emissions_kg_per_kg_h2" = c(output_list[[i]]$CH4),
                               "N2O_process_emissions_kg_per_kg_h2" = c(output_list[[i]]$N2O))
        } else {
          columns = data.frame("CO2_process_emissions_kg_per_kg_h2" = c(0), 
                               "CH4_process_emissions_kg_per_kg_h2" = c(0),
                               "N2O_process_emissions_kg_per_kg_h2" = c(0))
        }
        df_full = cbind(df_full,columns)
      } else if (values[i] == "total_upstream_emissions_kg_per_kg_h2") {
        x = 43
        print("!00")
        columns = data.frame("CO2_upstream_emissions_kg_per_kg_h2" = c(output_list[[i]]$CO2), 
                             "CH4_upstream_emissions_kg_per_kg_h2" = c(output_list[[i]]$CH4),
                             "N2O_upstream_emissions_kg_per_kg_h2" = c(output_list[[i]]$N2O))
        df_full = cbind(df_full,columns)
      }
    } else if (typeof(output_list[[i]]) %in% c("integer", "double") & length(output_list[[i]]) == 1) {
      #row = data.frame("variable" = c(values[i]), "value" = c(output_list[[i]]))
      column = data.frame("temp" = c(output_list[[i]]))
      colnames(column) = c(values[i])
      df_full = cbind(df_full,column)
    } else if (values[i] == "total_upstream_emissions_kg_per_kg_h2") {
      if (length(output_list[[i]]) > 0) {
        columns = data.frame("CO2_upstream_emissions_kg_per_kg_h2" = c(output_list[[i]][[1]]), 
                             "CH4_upstream_emissions_kg_per_kg_h2" = c(output_list[[i]][[2]]),
                             "N2O_upstream_emissions_kg_per_kg_h2" = c(output_list[[i]][[3]]))
      } else {
        columns = data.frame("CO2_upstream_emissions_kg_per_kg_h2" = c(0), 
                             "CH4_upstream_emissions_kg_per_kg_h2" = c(0),
                             "N2O_upstream_emissions_kg_per_kg_h2" = c(0))
      }
      df_full = cbind(df_full,columns)
    } else {
      #print(typeof(output_list[[i]]))
      t = 4
      # grapes
    }
    
    # look for double counting of electricity cost and set up a flag
    if (values[i] == "utilities") {
      found = c()
      for (j in output_list[[i]]) {
        found = c(found,j[[1]])
      }
      if ("Industrial Electricity" %in% found) {
        columns = data.frame("double_count" = c(1))
      } else {
        columns = data.frame("double_count" = c(0))
      }
      df_full = cbind(df_full,columns)
    }
    
    #print(values[i])
    #print(output_list[[i]])
    #print("---")
  }
  return(df_full)
}

cost_map = data.frame("long" = c(
  'dollars_per_kg_h2_capital_related_costs',
  'dollars_per_kg_h2_fixed_cost',
  'electricity_cost_per_kg_h2',
  'natural_gas_cost_per_kg_h2',
  'dollars_per_kg_h2_variable_cost',
  'dollars_per_kg_h2_other_raw_material_cost',
  'dollars_per_kg_h2_decommissioning_costs'), 
  "cost_segment" = c(
  'Capital',
  'Fixed',
  'Electricity',
  'Natural Gas',
  'Variable',
  'Other',
  'Other'
))

cost_barplot = function(results_filename) {
  columns = c(
    'model',
    'dollars_per_kg_h2_capital_related_costs',
    'dollars_per_kg_h2_fixed_cost',
    'electricity_cost_per_kg_h2',
    'natural_gas_cost_per_kg_h2',
    'dollars_per_kg_h2_variable_cost',
    'dollars_per_kg_h2_other_raw_material_cost',
    'dollars_per_kg_h2_decommissioning_costs',
    'double_count'
  )
  
  df = df %>% select(all_of(columns)) %>%
    # subtract electricity cost from variable cost if necessary
    mutate(dollars_per_kg_h2_variable_cost = dollars_per_kg_h2_variable_cost - (double_count * electricity_cost_per_kg_h2)) %>%
    select(-double_count) %>%
    pivot_longer(cols = 2:8, names_to = "long", values_to = "value") %>%
    left_join(cost_map, by = "long") %>%
    group_by(model, cost_segment) %>%
    summarize(value = sum(value)) %>%
    mutate(model = str_replace(model,".json","")) %>%
    mutate(model = str_replace(model,"default-","")) %>%
    mutate(model = str_replace(model,"-","\n")) %>%
    mutate(cost_segment = factor(cost_segment, 
                                 levels = c("Other", "Natural Gas", "Electricity", "Variable", "Fixed", "Capital")))
  
  sums = df %>% group_by(model) %>% summarize(value = sum(value))
  
  p = df %>% ggplot() +
    geom_bar(aes(x = model, y = value, fill = cost_segment), stat = "identity") +
    geom_text(aes(x = model, y = value, group = cost_segment, label = round(value,2)),
              hjust = 0.5, position = position_stack(vjust = 0.5),
              color = ifelse(df$cost_segment %in% c("Fixed", "Variable", "Electricity", "Natural Gas"), "white", "black"),
              alpha = ifelse(df$value < 0.05,0,1)) +
    geom_text(data = sums, aes(x = model, y = value, label = round(value,2)), vjust = -0.4, fontface = "bold") +
    labs(y = "Cost ($/kg H2)", title = "H2 Cost Comparison", fill = "Cost") +
    scale_fill_manual(values = c("Capital" = "#DAEDF4", "Electricity" = "black", "Fixed" = "#00008B", "Natural Gas" = "#008B8B", "Other" = "gray", "Variable" = "#9F0000")) +
    scale_y_continuous(expand = expansion(mult = c(0,.1))) +
    theme_classic() + 
    theme(axis.ticks = element_blank(), plot.title = element_text(hjust = 0.5),
          axis.title.x = element_blank())
              
  ggsave(filename = paste0("./output/plots/cost.png"), plot = p, width = 7, height = 5, units = "in")
  return(p)
}

emissions_barplot <- function(results_filename) {
  columns = c(
    'model',
    'CO2_process_emissions_kg_per_kg_h2',
    'CO2_Capture_Efficiency'
  )
  
  df = read.csv(paste0("./output/",results_filename))
  df = df %>% select(all_of(columns)) %>%
    mutate('Captured' = CO2_process_emissions_kg_per_kg_h2 * CO2_Capture_Efficiency,
           'Released' = CO2_process_emissions_kg_per_kg_h2 * (1 - CO2_Capture_Efficiency)) %>%
    select(c(model, Captured, Released)) %>%
    pivot_longer(cols = 2:3, names_to = "emissions", values_to = "value") %>%
    mutate(model = str_replace(model,".json","")) %>%
    mutate(model = str_replace(model,"default-","")) %>%
    mutate(model = str_replace(model,"-","\n"))
  
  sums = df %>% group_by(model) %>% summarize(value = sum(value, na.rm = TRUE))
  
  p = df %>% ggplot() +
    geom_bar(aes(x = model, y = value, fill = emissions), stat = "identity") +
    geom_text(aes(x = model, y = value, group = emissions, label = round(value,2)), 
              hjust = 0.5, position = position_stack(vjust = 0.5),
              color = ifelse(df$emissions == "Released", "white", "black"),
              alpha = ifelse(df$value == 0,0,1)) +
    geom_text(data = sums, aes(x = model, y = value, label = round(value,2)), vjust = -0.4, fontface = "bold") +
    labs(y = "CO2 Emissions (kg CO2 /kg H2)", title = "H2 Emissions Comparison", fill = "Emissions") +
    scale_y_continuous(expand = expansion(mult = c(0,.1))) +
    scale_fill_manual(values = c("Released" = "#00008B", "Captured" = "#DAEDF4")) +
    theme_classic() + 
    theme(axis.ticks = element_blank(), plot.title = element_text(hjust = 0.5),
          axis.title.x = element_blank())
  
  
  ggsave(filename = paste0("./output/plots/emissions.png"), plot = p, width = 7, height = 5, units = "in")
  return(p)
}

lifecycle_barplot <- function(results_filename) {
  columns = c(
    'model',
    'CO2_process_emissions_kg_per_kg_h2',
    'CO2_upstream_emissions_kg_per_kg_h2',
    'CO2_Capture_Efficiency'
  )
  
  df = read.csv(paste0("./output/",results_filename))
  df = df %>% select(all_of(columns)) %>%
    mutate('Direct' = CO2_process_emissions_kg_per_kg_h2 * (1 - CO2_Capture_Efficiency)) %>%
    rename("Upstream" = "CO2_upstream_emissions_kg_per_kg_h2") %>%
    select(c(model, Direct, Upstream)) %>%
    pivot_longer(cols = 2:3, names_to = "emissions", values_to = "value") %>%
    mutate(model = str_replace(model,".json","")) %>%
    mutate(model = str_replace(model,"default-","")) %>%
    mutate(model = str_replace(model,"-","\n")) %>%
    mutate(emissions = factor(emissions, levels = c("Upstream", "Direct")))
  
  sums = df %>% group_by(model) %>% summarize(value = sum(value, na.rm = TRUE))
  
  p = df %>% ggplot() +
    geom_bar(aes(x = model, y = value, fill = emissions), stat = "identity") +
    geom_text(aes(x = model, y = value, group = emissions, label = round(value,2)), 
              hjust = 0.5, position = position_stack(vjust = 0.5),
              color = ifelse(df$emissions == "Direct", "white", "black"),
              alpha = ifelse(df$value == 0,0,1)) +
    geom_text(data = sums, aes(x = model, y = value, label = round(value,2)), vjust = -0.4, fontface = "bold") +
    scale_fill_manual(values = c("Direct" = "#00008B", "Upstream" = "#DAEDF4")) +
    labs(y = "CO2 Emissions (kg CO2 /kg H2)", title = "H2 Emissions Comparison", fill = "Emissions") +
    scale_y_continuous(expand = expansion(mult = c(0,0.1))) +
    theme_classic() + 
    theme(axis.ticks = element_blank(), plot.title = element_text(hjust = 0.5),
          axis.title.x = element_blank())
  
  ggsave(filename = paste0("./output/plots/lifecycle.png"), plot = p, width = 7, height = 5, units = "in")
  return(p)
}

make_plots <- function(results_filename) {
  p = cost_barplot(results_filename)
  print(p)
  p = emissions_barplot(results_filename)
  print(p)
  p = lifecycle_barplot(results_filename)
  print(p)
}

