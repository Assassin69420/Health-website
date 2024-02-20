from django import forms


class NewOfferForm(forms.Form):
    CATEGORIES = (
        (1, "Nutrition"),
        (2, "Fitness"),
        (3, "Sports"),
        (4, "Gym"),
    )

    name = forms.CharField()
    description = forms.CharField()
    price = forms.DecimalField(decimal_places=2, widget=forms.NumberInput)
    category = forms.ChoiceField(choices=CATEGORIES, widget=forms.RadioSelect)
    image = forms.ImageField()


class EditOfferForm(forms.Form):
    CATEGORIES = (
        (1, "Nutrition"),
        (2, "Fitness"),
        (3, "Sports"),
        (4, "Gym"),
    )

    name = forms.CharField()
    description = forms.CharField()
    price = forms.DecimalField(decimal_places=2, widget=forms.NumberInput)
    category = forms.ChoiceField(choices=CATEGORIES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        item = kwargs.pop("item", None)
        super(EditOfferForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['description'].required = False
        self.fields['price'].required = False
        self.fields['category'].required = False
        

        if item:
            self.fields["name"].widget.attrs["placeholder"] = item.name
            self.fields["description"].widget.attrs["placeholder"] = item.description
            self.fields["price"].widget.attrs["placeholder"] = item.price 
