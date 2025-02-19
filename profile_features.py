import csv_read_write
import check_phone_number
import check_offensive
import check_age
import check_budget
import check_email
import pandas as pd


def get_binary_result(input_list):
    result = []
    for row in input_list:
        if str(row) == "nan":
            output = 0
        else:
            output = 1
        result.append(output)
    return result


def get_label(path):
    dataframe = pd.read_csv(path, low_memory=False)
    status_binary = dataframe["status_label"].tolist()
    status_result = []
    for row in status_binary:
        if str(row) == "Dead":
            result = 0
        else:
            result = 1
        status_result.append(result)
    csv_read_write.list_write_csv("data/label.csv", "status_binary", status_result)


def profile_features_extraction(path):
    path_write_to = "data/profile_features.csv"
    dataframe = pd.read_csv(path, low_memory=False)
    age_16_list = dataframe["custom.Older than 16"].tolist()
    age_18_list = dataframe["custom.Older Than 18"].tolist()
    name_list = dataframe["primary_contact_name"].tolist()
    phone_list = dataframe["primary_contact_primary_phone"].tolist()
    email_list = dataframe["primary_contact_primary_email"].tolist()
    city_list = dataframe["custom.City"].tolist()
    cartype_list = dataframe[
        "custom.Fantastic, what kind of *car* are you looking to buy, {{field:25546809ff208152}}?"].tolist()
    total_budget_list = dataframe["custom.Total Budget"].tolist()
    biweekly_budget_list = dataframe["custom.Bi-Weekly Budget"].tolist()
    check_budget_list = check_budget.check_budget(total_budget_list,
                                                  biweekly_budget_list,
                                                  40000, # threshold_total_budget_high,
                                                  10000, # threshold_total_budget_low,
                                                  450, # threshold_biweekly_budget_high,
                                                  150) #  threshold_biweekly_budget_low)
    check_cartype_list = check_budget.check_cartype(cartype_list,"EV, SUV, Truck") # high_level_cartype

    priority_label = dict(P1=check_phone_number.fake_phone_check(phone_list, 6), # threshold_phone_fake),
                          P2=check_phone_number.check_phone_area_code(phone_list, "reference/reference_area_code.csv"),
                          P3=check_email.check_email_format(email_list),
                          P4=check_offensive.offensive_detect(email_list, "reference/reference_offensive_word.csv"),
                          P5=check_offensive.offensive_detect(name_list, "reference/reference_offensive_word.csv"),
                          P6=check_offensive.offensive_detect(city_list, "reference/reference_offensive_word.csv"),
                          P10=check_age.check_age(age_16_list, age_18_list),
                          P12=check_budget_list,
                          P13=check_cartype_list,
                          P14=check_budget.check_budget_cartype(check_budget_list, check_cartype_list),
                          P15=check_email.check_email_name(email_list, name_list),
                          P16=check_email.check_email_age(email_list, age_16_list,
                                                          age_18_list),
                          )

    # phone
    csv_read_write.list_write_csv(path_write_to, "if the phone number is real ", priority_label["P1"])
    csv_read_write.list_write_csv(path_write_to, "if the area code from phone number is real", priority_label["P2"])

    # email
    csv_read_write.list_write_csv(path_write_to, "if the email address format is real", priority_label["P3"])

    # offensive
    csv_read_write.list_write_csv(path_write_to, "if the email address contains offensive word", priority_label["P4"])
    csv_read_write.list_write_csv(path_write_to, "if the customer name contains offensive word", priority_label["P5"])
    csv_read_write.list_write_csv(path_write_to, "if the city name contains offensive word", priority_label["P6"])

    # age
    csv_read_write.list_write_csv(path_write_to, "if the customer is adult ", priority_label["P10"])

    # budget
    csv_read_write.list_write_csv(path_write_to, "if the customer want an expensive car type", priority_label["P12"])
    csv_read_write.list_write_csv(path_write_to, "if the customer have a high budget", priority_label["P13"])
    csv_read_write.list_write_csv(path_write_to, "if the customer want an expensive car type with low budget",
                                  priority_label["P14"])

    csv_read_write.list_write_csv(path_write_to, "if the email address contains customer's name", priority_label["P15"])
    csv_read_write.list_write_csv(path_write_to, "if the birth year from email address match their age",
                                  priority_label["P16"])

    bodytype_binary = dataframe["custom.Body Type"].tolist()
    purchase_binary = dataframe["custom.Choice of Purchase"].tolist()
    city_binary = dataframe["custom.City"].tolist()
    drivetype_binary = dataframe["custom.Drive type"].tolist()
    cartype_binary = dataframe[
        "custom.Fantastic, what kind of *car* are you looking to buy, {{field:25546809ff208152}}?"].tolist()
    followup_binary = dataframe["custom.Follow up"].tolist()
    fueltype_binary = dataframe["custom.Fuel Type"].tolist()
    interior_binary = dataframe["custom.Interior Colours"].tolist()
    make_binary = dataframe["custom.Make"].tolist()
    model_binary = dataframe["custom.Model"].tolist()
    motivation_binary = dataframe["custom.Motivation"].tolist()
    notes_binary = dataframe["custom.Notes"].tolist()
    occupation_binary = dataframe["custom.Occupation"].tolist()
    recreation_binary = dataframe["custom.Recreation"].tolist()
    stock_binary = dataframe["custom.Stock Number"].tolist()
    totalbudget_binary = dataframe["custom.Total Budget"].tolist()
    transmission_binary = dataframe["custom.Transmission"].tolist()
    trim_binary = dataframe["custom.Trim"].tolist()
    vin_binary = dataframe["custom.VIN"].tolist()
    year_binary = dataframe["custom.Year"].tolist()

    csv_read_write.list_write_csv(path_write_to, "bodytype_binary", get_binary_result(bodytype_binary))
    csv_read_write.list_write_csv(path_write_to, "purchase_binary", get_binary_result(purchase_binary))
    csv_read_write.list_write_csv(path_write_to, "city_binary", get_binary_result(city_binary))
    csv_read_write.list_write_csv(path_write_to, "drivetype_binary",
                                  get_binary_result(drivetype_binary))
    csv_read_write.list_write_csv(path_write_to, "cartype_binary",
                                  get_binary_result(cartype_binary))
    csv_read_write.list_write_csv(path_write_to, "followup_binary",
                                  get_binary_result(followup_binary))
    csv_read_write.list_write_csv(path_write_to, "fueltype_binary",
                                  get_binary_result(fueltype_binary))
    csv_read_write.list_write_csv(path_write_to, "interior_binary",
                                  get_binary_result(interior_binary))
    csv_read_write.list_write_csv(path_write_to, "city_binary", get_binary_result(city_binary))
    csv_read_write.list_write_csv(path_write_to, "make_binary",
                                  get_binary_result(make_binary))
    csv_read_write.list_write_csv(path_write_to, "model_binary",
                                  get_binary_result(model_binary))
    csv_read_write.list_write_csv(path_write_to, "motivation_binary",
                                  get_binary_result(motivation_binary))
    csv_read_write.list_write_csv(path_write_to, "notes_binary",
                                  get_binary_result(notes_binary))
    csv_read_write.list_write_csv(path_write_to, "occupation_binary",
                                  get_binary_result(occupation_binary))
    csv_read_write.list_write_csv(path_write_to, "recreation_binary",
                                  get_binary_result(recreation_binary))
    csv_read_write.list_write_csv(path_write_to, "stock_binary",
                                  get_binary_result(stock_binary))
    csv_read_write.list_write_csv(path_write_to, "totalbudget_binary",
                                  get_binary_result(totalbudget_binary))
    csv_read_write.list_write_csv(path_write_to, "transmission_binary",
                                  get_binary_result(transmission_binary))
    csv_read_write.list_write_csv(path_write_to, "trim_binary",
                                  get_binary_result(trim_binary))
    csv_read_write.list_write_csv(path_write_to, "vin_binary",
                                  get_binary_result(vin_binary))
    csv_read_write.list_write_csv(path_write_to, "year_binary",
                                  get_binary_result(year_binary))

#get_label("data/training_data.csv")
#profile_features_extraction("data/training_data.csv")