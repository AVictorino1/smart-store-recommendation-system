

def best_recommendations(product, all_products):

    recomm = dict()

    similar_price = 1
    similar_brand = 2
    similar_category = 3
    
    for similar in all_products:
        if similar["id"] != product["id"]:
            

            #Same brand and category
            if similar["brand"] == product["brand"]:
                if similar["id"] not in recomm:
                    recomm[similar["id"]] = 0
                recomm[similar["id"]] += similar_brand

            if similar["category"] == product["category"]:
                if similar["id"] not in recomm:
                    recomm[similar["id"]] = 0
                recomm[similar["id"]] += similar_category

            #Almost same price
            
            difference = abs(similar["price"] - product["price"])
            price_per = (difference / int(product["price"])) * 100
            
            #Exact same price
            if similar["price"] == product["price"]:
                if similar["id"] not in recomm:
                    recomm[similar["id"]] = 0
                recomm[similar["id"]] += similar_price 
            elif price_per <= 5:
                if similar["id"] not in recomm:
                    recomm[similar["id"]] = 0
                recomm[similar["id"]] += similar_price
            elif 5 < price_per <= 10:
                if similar["id"] not in recomm:
                    recomm[similar["id"]] = 0
                recomm[similar["id"]] += similar_price * 0.60
            elif 10 < price_per <= 20:
                if similar["id"] not in recomm:
                    recomm[similar["id"]] = 0
                recomm[similar["id"]] += similar_price * 0.30
    
    best_recomm = sorted(recomm.items(), key = lambda item: item[1], reverse =True)

    best_recomm_l = best_recomm[:3]


    best_prod = []

    for x in best_recomm_l:
        best_prod.append(x[0])

    return best_prod
