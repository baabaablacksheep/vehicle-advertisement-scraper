class Vehicle:
    def __init__(self, ad_url, ad_title, brand, model, model_year, body_type, image_url_list):
        self.ad_url = ad_url
        self.ad_title = ad_title.lower()
        self.brand = brand.lower()
        self.model = model.lower()
        self.model_year = model_year
        self.body_type = body_type.lower()
        self.image_url_list = image_url_list

    def showInfo(self):
        print("Ad Url: " + self.ad_url)
        print("Ad Title: " + self.ad_title)
        print("Brand: " + self.brand)
        print("Model: " + self.model)
        print("Model Year: " + self.model_year)
        print("Body Type: " + self.body_type)
        print("Image URLs: ")
        for img in self.image_url_list:
            print("  "+img)
