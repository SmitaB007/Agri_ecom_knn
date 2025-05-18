from store.models import Product,Profile

class Cart():
    def __init__(self,request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key']={}

        self.cart = cart

    def db_add(self,product,quantity):
        
        product_id = str(product)
      
        product_qty = int(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=product_qty
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            car = str(self.cart)
            car = car.replace("\'","\"")
            current_user.update(old_cart=str(car))

    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=product_qty
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            car = str(self.cart)
            car = car.replace("\'","\"")
            
            current_user.update(old_cart=str(car))

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        total_products = Product.objects.filter(id__in=product_ids)
        return total_products

    def get_qty(self):
        qty = self.cart
        return qty
    
    def delete_prod(self,product):
        product_id = str(product)
        car = self.cart
        if product_id in self.cart:
           car.pop(product_id)

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            car = str(self.cart)
            car = car.replace("\'","\"")
            current_user.update(old_cart=str(car))
        self.session.modified = True

    def update(self,product,quantity):
        product_id = str(product)
        car = self.cart
        qty = int(quantity)
        if product_id in self.cart:
         car[product_id] = qty
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            car = str(self.cart)
            car = car.replace("\'","\"")
            current_user.update(old_cart=str(car))

        self.session.modified = True


    def get_amount(self):
        quantities = self.cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        tax=0
        delivery=0
        for k,v in quantities.items():
            key = int(k)
            for product in products:

                delivery =  product.delivery_charges 
                if key == product.id:
                    if product.is_sale:
                       
                        total = total+(product.sale_price*v)
                        tax = tax+int(product.category.tax)
                        delivery = product.delivery
                        
                        

                    else:
                        
                        total = total+(product.price * v)
                        print(total)
                        tax = tax+product.category.tax
                        delivery = product.delivery_charges


                      

                        

                        
        total = total+((total*tax)/100)        
        total = total+delivery
        print("Tax",tax)
        print("delivery",delivery)

                   
            
      
                
        return total,tax,delivery

                
    
    def cal(self,argument,t):
        
        match argument:
            case "Biological Fertilizers":
                    t =  (t*5)/100
                    return t
            case "Liquid Fertilizers":
                    t = (t*5)/100
                    return t
            case "Micronutrient Fertilizers":
                    t =  (t*5)/100
                    return t
            case "Organic Fertilizers":
                    t =  (t*5)/100
                    return t
            case "Soil Application":
                    t =  (t*5)/100
                    return t
            case "Fodder seed":
                    t =  (t*5)/100
                    return t
            case "Goat and sheep care ":
                   t =  (t*5)/100
                   return t
            case "Machinery":
                    t =  (t*5)/100
                    return t
            case "Bactericides":
                    t =  (t*5)/100
                    return t
            case "Bio-Pesticides":
                    t =  (t*5)/100
                    return t
            case "Fungicides":
                    t = (t*5)/100
                    return t
            case "Herbicides":
                    t = (t*5)/100
                    return t
            case "Insecticides":
                    t =  (t*5)/100
                    return t
            case "Cotton seeds":
                    t = (t*5)/100
                    return t
            case "Exotic Vegetables":
                    t =  (t*5)/100
                    return t
            case "Field Crop seeds ":
                    t =  (t*5)/100
                    return t
            case "Leafy Vegetables":
                    t =  (t*5)/100
                    return t
            case "Pulse seeds":
                    t =  (t*5)/100
                    return t
            case "Vegetables":
                    t =  (t*5)/100
                    return t
            case "Fruit Crop":
                    t = (t*5)/100
                    return t
            

                
                 
