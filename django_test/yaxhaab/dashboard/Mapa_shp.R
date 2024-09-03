sf_san <- sf::read_sf("~/Downloads/Shp_SnJeCoatlan_PMF_2019_/Shp_SnJeCoatlan_PMF_2019_.shp")
sf_use_s2(F)
temp <- sf_san %>% 
  mutate(clase = case_when(
    TV == "Selva Baja Subcaducifolia" ~"Selva Baja",
    CLAS_SUP_1 == "Sup Producción en Reserva" ~ "Bosque no Maderable",
    CLAS_SUP_1 == "Sup Producción Maderable PMF 2017-2027" ~ "Bosque Maderable",
    CLAS_SUP_1 == "Sup Producción Maderable PMF 2019-2028" ~ "Bosque Maderable",
    CLAS_SUP_1 == "Agricultura de temporal" ~ "Agricultura y Ganadería",
    CLAS_SUP_1 == "Areas de Restauración" ~ "Reservas y Restauración",
    CLAS_SUP_1 == "Pastizal inducido" ~ "Agricultura y Ganadería",
    CLAS_SUP_1 == "Superficies con pendientes mayores al 100%" ~ "Bosque no Maderable",
    CLAS_SUP_1 == "Zona Urbana" ~ "Urbano",
    CLAS_SUP_1 == "Superficies con vegetaión de manglar o BMM" ~ "Bosque Mesófilo",
    CLAS_SUP_1 == "Areas Naturales Comunitarias protegidas" ~ "Reservas y Restauración",
    CLAS_SUP_1 == "Superficies para proteger y Conservar el Habitat de Flora y Fauna" ~ "Reservas y Restauración",
  ),
  RODAL = ifelse(clase == "Bosque Maderable","Rodal: "%+% RODAL%+%"\n", ""),
  
  ) %>% 
  group_by(clase,RODAL) %>% 
  summarise(
            geometry = sf::st_union(geometry),
            superficie = sum(SUP_HA)) %>% 
  ungroup() %>% 
  mutate(
         geometry = sf::st_make_valid(geometry),
         geometry = sf::st_transform(geometry,crs = "WGS84"),
         ) %>%  
  mutate(geometry = sf::st_union(geometry,by_feature = T))

library(tmap)
tmap_options(check.and.fix = TRUE) 
sf_use_s2(F)
temp %>% st_crs()
temp %>% 
  mutate(geometry = st_simplify(st_transform(geometry, "EPSG:4087"),dTolerance = 100)) %>% 
 tm_shape() + tm_polygons(col = "clase")


temp_casted <- temp %>%
  ungroup() %>% 
  sf::st_cast("MULTIPOLYGON") %>% 
  sf::st_cast("POLYGON") %>% 
  sf::st_cast("POLYGON") %>% 
  rowid_to_column() %>% 
  mutate(superficie = st_area(geometry),
         superficie = units::set_units(superficie,ha),
         superficie = round(superficie, 1))

temp_casted %>% 
  geojsonio::topojson_write(geometry = "polygon",
                            file = "~/django_local_library/django_test/yaxhaab/dashboard/static/assets/sjc.json",
                            #convert_wgs84 = T,
                            group ="id",
                            object_name = "zonas",quantization = 1e4)


temp
temp %>% as_tibble() %>% dplyr::count(clase)
