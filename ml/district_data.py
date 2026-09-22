"""
Comprehensive Indian States and Districts Data Repository
Provides complete mapping of 28 States and 8 Union Territories to their administrative districts,
along with geographic centroids for microclimatic precision in agricultural predictions.
"""

# Complete District Mapping for All 28 Indian States & 8 Union Territories
STATE_DISTRICTS = {
    "Andhra Pradesh": [
        "Alluri Sitharama Raju", "Anakapalli", "Ananthapuramu", "Annamayya", "Bapatla",
        "Chittoor", "East Godavari", "Eluru", "Guntur", "Kakinada", "Konaseema",
        "Krishna", "Kurnool", "Nandyal", "NTR", "Palnadu", "Parvathipuram Manyam",
        "Prakasam", "Sri Potti Sriramulu Nellore", "Sri Sathya Sai", "Srikakulam",
        "Tirupati", "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa"
    ],
    "Arunachal Pradesh": [
        "Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang",
        "Kamle", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit",
        "Longding", "Lower Dibang Valley", "Lower Siang", "Lower Subansiri",
        "Namsai", "Pakke Kessang", "Papum Pare", "Shi Yomi", "Siang",
        "Tawang", "Tirap", "Upper Siang", "Upper Subansiri", "West Kameng", "West Siang"
    ],
    "Assam": [
        "Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", "Charaideo",
        "Chirang", "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Dima Hasao",
        "Goalpara", "Golaghat", "Hailakandi", "Hojai", "Jorhat", "Kamrup",
        "Kamrup Metropolitan", "Karbi Anglong", "Karimganj", "Kokrajhar",
        "Lakhimpur", "Majuli", "Morigaon", "Nagaon", "Nalbari", "Sivasagar",
        "Sonitpur", "South Salmara-Mankachar", "Tinsukia", "Udalguri", "West Karbi Anglong"
    ],
    "Bihar": [
        "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur",
        "Bhojpur", "Buxar", "Darbhanga", "East Champaran", "Gaya", "Gopalganj",
        "Jamui", "Jehanabad", "Kaimur", "Katihar", "Khagaria", "Kishanganj",
        "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur", "Nalanda",
        "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa", "Samastipur", "Saran",
        "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan", "Supaul", "Vaishali", "West Champaran"
    ],
    "Chhattisgarh": [
        "Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", "Bijapur",
        "Bilaspur", "Dantewada", "Dhamtari", "Durg", "Gariaband", "Gaurela Pendra Marwahi",
        "Janjgir-Champa", "Jashpur", "Kabirdham", "Kanker", "Khairagarh", "Kondagaon",
        "Korba", "Koriya", "Mahasamund", "Manendragarh", "Mohla Manpur", "Mungeli",
        "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon", "Sarangarh", "Sukma",
        "Surajpur", "Surguja"
    ],
    "Goa": [
        "North Goa", "South Goa"
    ],
    "Gujarat": [
        "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch",
        "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod", "Dang", "Devbhoomi Dwarka",
        "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda", "Kutch",
        "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal",
        "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar",
        "Tapi", "Vadodara", "Valsad"
    ],
    "Haryana": [
        "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", "Gurugram",
        "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra", "Mahendragarh",
        "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari", "Rohtak", "Sirsa",
        "Sonipat", "Yamunanagar"
    ],
    "Himachal Pradesh": [
        "Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu",
        "Lahaul and Spiti", "Mandi", "Shimla", "Sirmaur", "Solan", "Una"
    ],
    "Jharkhand": [
        "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum",
        "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara",
        "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu",
        "Ramgarh", "Ranchi", "Sahibganj", "Seraikela Kharsawan", "Simdega", "West Singhbhum"
    ],
    "Karnataka": [
        "Bagalkote", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
        "Bidar", "Chamarajanagar", "Chikkaballapura", "Chikkamagaluru", "Chitradurga",
        "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri",
        "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru", "Raichur",
        "Ramanagara", "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada", "Vijayanagara",
        "Vijayapura", "Yadgir"
    ],
    "Kerala": [
        "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam",
        "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta",
        "Thiruvananthapuram", "Thrissur", "Wayanad"
    ],
    "Madhya Pradesh": [
        "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", "Barwani",
        "Betul", "Bhind", "Bhopal", "Burhanpur", "Chhatarpur", "Chhindwara",
        "Damoh", "Datia", "Dewas", "Dhar", "Dindori", "Guna", "Gwalior", "Harda",
        "Hoshangabad (Narmadapuram)", "Indore", "Jabalpur", "Jhabua", "Katni",
        "Khandwa", "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur",
        "Neemuch", "Niwari", "Panna", "Raisen", "Rajgarh", "Ratlam", "Rewa",
        "Sagar", "Satna", "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur",
        "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha"
    ],
    "Maharashtra": [
        "Ahmednagar (Ahilyanagar)", "Akola", "Amravati", "Aurangabad (Chhatrapati Sambhajinagar)",
        "Beed", "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", "Gondia",
        "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban",
        "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad (Dharashiv)", "Palghar",
        "Parbhani", "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara", "Sindhudurg",
        "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"
    ],
    "Manipur": [
        "Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West",
        "Jiribam", "Kakching", "Kamjong", "Kangpokpi", "Noney", "Pherzawl",
        "Senapati", "Tamenglong", "Tengnoupal", "Thoubal", "Ukhrul"
    ],
    "Meghalaya": [
        "East Garo Hills", "East Jaintia Hills", "East Khasi Hills", "Eastern West Khasi Hills",
        "North Garo Hills", "Ri Bhoi", "South Garo Hills", "South West Garo Hills",
        "South West Khasi Hills", "West Garo Hills", "West Jaintia Hills", "West Khasi Hills"
    ],
    "Mizoram": [
        "Aizawl", "Champhai", "Hnahthial", "Khawzawl", "Kolasib", "Lawngtlai",
        "Lunglei", "Mamit", "Saitual", "Serchhip", "Siaha"
    ],
    "Nagaland": [
        "Chumoukedima", "Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung",
        "Mon", "Niuland", "Noklak", "Peren", "Phek", "Shamator", "Tseminyu",
        "Tuensang", "Wokha", "Zunheboto"
    ],
    "Odisha": [
        "Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh",
        "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur",
        "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Kendujhar",
        "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh",
        "Nuapada", "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundargarh"
    ],
    "Punjab": [
        "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib",
        "Fazilka", "Firozpur", "Gurdaspur", "Hoshiarpur", "Jalandhar",
        "Kapurthala", "Ludhiana", "Malerkotla", "Mansa", "Moga", "Muktsar",
        "Pathankot", "Patiala", "Rupnagar", "Sahibzada Ajit Singh Nagar (Mohali)",
        "Sangrur", "Shahid Bhagat Singh Nagar (Nawanshahr)", "Tarn Taran"
    ],
    "Rajasthan": [
        "Ajmer", "Alwar", "Anupgarh", "Balotra", "Banswara", "Baran", "Barmer",
        "Beawar", "Bharatpur", "Bhilwara", "Bikaner", "Bundi", "Chittorgarh",
        "Churu", "Dausa", "Deeg", "Dholpur", "Didwana-Kuchaman", "Dudu",
        "Dungarpur", "Ganganagar", "Gangapur City", "Hanumangarh", "Jaipur",
        "Jaipur Rural", "Jaisalmer", "Jalore", "Jhalawar", "Jhunjhunu", "Jodhpur",
        "Jodhpur Rural", "Karauli", "Kekri", "Khairthal-Tijara", "Kota", "Kotputli-Behror",
        "Nagaur", "Neem Ka Thana", "Pali", "Phalodi", "Pratapgarh", "Rajsamand",
        "Salumbar", "Sanchore", "Sawai Madhopur", "Shahpura", "Sikar", "Sirohi",
        "Tonk", "Udaipur"
    ],
    "Sikkim": [
        "Gangtok", "Gyalshing", "Mangan", "Namchi", "Pakyong", "Soreng"
    ],
    "Tamil Nadu": [
        "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
        "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram",
        "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
        "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
        "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi", "Thanjavur",
        "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur",
        "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
        "Viluppuram", "Virudhunagar"
    ],
    "Telangana": [
        "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad", "Jagtial",
        "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy",
        "Karimnagar", "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad",
        "Mahabubnagar", "Mancherial", "Medak", "Medchal-Malkajgiri", "Mulugu",
        "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad",
        "Peddapalli", "Rajanna Sircilla", "Ranga Reddy", "Sangareddy", "Siddipet",
        "Suryapet", "Vikarabad", "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri"
    ],
    "Tripura": [
        "Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala",
        "South Tripura", "Unakoti", "West Tripura"
    ],
    "Uttar Pradesh": [
        "Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", "Auraiya",
        "Ayodhya", "Azamgarh", "Baghpat", "Bahraich", "Ballia", "Balrampur",
        "Banda", "Barabanki", "Bareilly", "Basti", "Bhadohi", "Bijnor",
        "Budaun", "Bulandshahr", "Chandauli", "Chitrakoot", "Deoria", "Etah",
        "Etawah", "Farrukhabad", "Fatehpur", "Firozabad", "Gautam Buddha Nagar",
        "Ghaziabad", "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", "Hapur",
        "Hardoi", "Hathras", "Jalaun", "Jaunpur", "Jhansi", "Kannauj",
        "Kanpur Dehat", "Kanpur Nagar", "Kasganj", "Kaushambi", "Kheri",
        "Kushinagar", "Lalitpur", "Lucknow", "Maharajganj", "Mahoba", "Mainpuri",
        "Mathura", "Mau", "Meerut", "Mirzapur", "Moradabad", "Muzaffarnagar",
        "Pilibhit", "Pratapgarh", "Prayagraj", "Raebareli", "Rampur", "Saharanpur",
        "Sambhal", "Sant Kabir Nagar", "Shahjahanpur", "Shamli", "Shrawasti",
        "Siddharthnagar", "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"
    ],
    "Uttarakhand": [
        "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar",
        "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag", "Tehri Garhwal",
        "Udham Singh Nagar", "Uttarkashi"
    ],
    "West Bengal": [
        "Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur",
        "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram", "Kalimpong",
        "Kolkata", "Malda", "Murshidabad", "Nadia", "North 24 Parganas",
        "Paschim Bardhaman", "Paschim Medinipur", "Purba Bardhaman", "Purba Medinipur",
        "Purulia", "South 24 Parganas", "Uttar Dinajpur"
    ],
    "Andaman and Nicobar Islands": [
        "Nicobar", "North and Middle Andaman", "South Andaman"
    ],
    "Chandigarh": [
        "Chandigarh"
    ],
    "Dadra and Nagar Haveli and Daman and Diu": [
        "Dadra and Nagar Haveli", "Daman", "Diu"
    ],
    "Delhi": [
        "Central Delhi", "East Delhi", "New Delhi", "North Delhi", "North East Delhi",
        "North West Delhi", "Shahdara", "South Delhi", "South East Delhi",
        "South West Delhi", "West Delhi"
    ],
    "Jammu and Kashmir": [
        "Anantnag", "Bandipora", "Baramulla", "Budgam", "Doda", "Ganderbal",
        "Jammu", "Kathua", "Kishtwar", "Kulgam", "Kupwara", "Poonch", "Pulwama",
        "Rajouri", "Ramban", "Reasi", "Samba", "Shopian", "Srinagar", "Udhampur"
    ],
    "Ladakh": [
        "Kargil", "Leh"
    ],
    "Lakshadweep": [
        "Lakshadweep"
    ],
    "Puducherry": [
        "Karaikal", "Mahe", "Puducherry", "Yanam"
    ]
}

# Major Agricultural District Coordinates for Hyper-Local Weather Queries
DISTRICT_COORDINATES = {
    # Punjab
    ("Punjab", "Ludhiana"): (30.9010, 75.8573),
    ("Punjab", "Amritsar"): (31.6340, 74.8723),
    ("Punjab", "Bathinda"): (30.2110, 74.9455),
    ("Punjab", "Patiala"): (30.3398, 76.3869),
    ("Punjab", "Jalandhar"): (31.3260, 75.5762),
    ("Punjab", "Firozpur"): (30.9237, 74.6114),
    ("Punjab", "Sangrur"): (30.2458, 75.8421),

    # Maharashtra
    ("Maharashtra", "Nashik"): (19.9975, 73.7898),
    ("Maharashtra", "Nagpur"): (21.1458, 79.0882),
    ("Maharashtra", "Pune"): (18.5204, 73.8567),
    ("Maharashtra", "Kolhapur"): (16.7050, 74.2433),
    ("Maharashtra", "Ahmednagar (Ahilyanagar)"): (19.0952, 74.7496),
    ("Maharashtra", "Solapur"): (17.6599, 75.9064),
    ("Maharashtra", "Amravati"): (20.9320, 77.7523),
    ("Maharashtra", "Jalgaon"): (21.0077, 75.5626),

    # Uttar Pradesh
    ("Uttar Pradesh", "Muzaffarnagar"): (29.4727, 77.7085),
    ("Uttar Pradesh", "Meerut"): (28.9845, 77.7064),
    ("Uttar Pradesh", "Varanasi"): (25.3176, 82.9739),
    ("Uttar Pradesh", "Gorakhpur"): (26.7606, 83.3732),
    ("Uttar Pradesh", "Bareilly"): (28.3670, 79.4304),
    ("Uttar Pradesh", "Aligarh"): (27.8974, 78.0880),
    ("Uttar Pradesh", "Prayagraj"): (25.4358, 81.8463),
    ("Uttar Pradesh", "Lucknow"): (26.8467, 80.9462),

    # West Bengal
    ("West Bengal", "Purba Bardhaman"): (23.2324, 87.8615),
    ("West Bengal", "Hooghly"): (22.9034, 88.3965),
    ("West Bengal", "Nadia"): (23.4710, 88.5565),
    ("West Bengal", "Murshidabad"): (24.1759, 88.2802),
    ("West Bengal", "Malda"): (25.0108, 88.1411),
    ("West Bengal", "Darjeeling"): (27.0410, 88.2663),

    # Andhra Pradesh
    ("Andhra Pradesh", "Guntur"): (16.3067, 80.4365),
    ("Andhra Pradesh", "Krishna"): (16.1875, 81.1389),
    ("Andhra Pradesh", "East Godavari"): (17.0005, 81.8040),
    ("Andhra Pradesh", "West Godavari"): (16.7107, 81.0952),
    ("Andhra Pradesh", "Kurnool"): (15.8281, 78.0373),
    ("Andhra Pradesh", "Ananthapuramu"): (14.6819, 77.6006),

    # Karnataka
    ("Karnataka", "Kolar"): (13.1367, 78.1291),
    ("Karnataka", "Mandya"): (12.5244, 76.8958),
    ("Karnataka", "Belagavi"): (15.8497, 74.4977),
    ("Karnataka", "Mysuru"): (12.2958, 76.6394),
    ("Karnataka", "Dharwad"): (15.4589, 75.0078),
    ("Karnataka", "Shivamogga"): (13.9299, 75.5681),

    # Tamil Nadu
    ("Tamil Nadu", "Thanjavur"): (10.7870, 79.1378),
    ("Tamil Nadu", "Coimbatore"): (11.0168, 76.9558),
    ("Tamil Nadu", "Madurai"): (9.9252, 78.1198),
    ("Tamil Nadu", "Salem"): (11.6643, 78.1460),
    ("Tamil Nadu", "Erode"): (11.3410, 77.7172),

    # Gujarat
    ("Gujarat", "Anand"): (22.5645, 72.9289),
    ("Gujarat", "Rajkot"): (22.3039, 70.8022),
    ("Gujarat", "Junagadh"): (21.5222, 70.4579),
    ("Gujarat", "Mehsana"): (23.5880, 72.3693),
    ("Gujarat", "Surat"): (21.1702, 72.8311),

    # Rajasthan
    ("Rajasthan", "Ganganagar"): (29.9038, 73.8772),
    ("Rajasthan", "Kota"): (25.2138, 75.8648),
    ("Rajasthan", "Jaipur"): (26.9124, 75.7873),
    ("Rajasthan", "Bikaner"): (28.0229, 73.3119),
    ("Rajasthan", "Jodhpur"): (26.2389, 73.0243),

    # Jammu and Kashmir
    ("Jammu and Kashmir", "Shopian"): (33.7208, 74.8325),
    ("Jammu and Kashmir", "Baramulla"): (34.2046, 74.3436),
    ("Jammu and Kashmir", "Anantnag"): (33.7311, 75.1524),
    ("Jammu and Kashmir", "Srinagar"): (34.0837, 74.7973),
    ("Jammu and Kashmir", "Jammu"): (32.7266, 74.8570),

    # Haryana
    ("Haryana", "Karnal"): (29.6857, 76.9905),
    ("Haryana", "Hisar"): (29.1492, 75.7217),
    ("Haryana", "Sirsa"): (29.5349, 75.0289),
    ("Haryana", "Kurukshetra"): (29.9695, 76.8783),

    # Madhya Pradesh
    ("Madhya Pradesh", "Indore"): (22.7196, 75.8577),
    ("Madhya Pradesh", "Ujjain"): (23.1765, 75.7885),
    ("Madhya Pradesh", "Hoshangabad (Narmadapuram)"): (22.7519, 77.7289),
    ("Madhya Pradesh", "Gwalior"): (26.2183, 78.1828),

    # Bihar
    ("Bihar", "Muzaffarpur"): (26.1209, 85.3647),
    ("Bihar", "Nalanda"): (25.1982, 85.5149),
    ("Bihar", "Bhagalpur"): (25.2425, 86.9842),
    ("Bihar", "Patna"): (25.5941, 85.1376),

    # Kerala
    ("Kerala", "Palakkad"): (10.7867, 76.6548),
    ("Kerala", "Wayanad"): (11.6854, 76.1320),
    ("Kerala", "Idukki"): (9.8494, 76.9804),
    ("Kerala", "Alappuzha"): (9.4981, 76.3388),

    # Telangana
    ("Telangana", "Karimnagar"): (18.4386, 79.1288),
    ("Telangana", "Nizamabad"): (18.6725, 78.0941),
    ("Telangana", "Warangal"): (17.9689, 79.5941),
    ("Telangana", "Nalgonda"): (17.0577, 79.2684),
}


def get_districts_for_state(state):
    """Return list of sorted districts for the given Indian state or UT."""
    if not state:
        return []
    
    # Try exact match first
    if state in STATE_DISTRICTS:
        return STATE_DISTRICTS[state]
    
    # Case-insensitive match
    for st, districts in STATE_DISTRICTS.items():
        if st.lower() == state.lower():
            return districts
            
    return []


def get_district_coords(state, district):
    """
    Return (latitude, longitude) tuple for a given (state, district).
    Returns None if specific district centroid is not mapped.
    """
    if not state or not district:
        return None
        
    # Check exact tuple
    coords = DISTRICT_COORDINATES.get((state, district))
    if coords:
        return coords
        
    # Case-insensitive search
    for (st, dist), c in DISTRICT_COORDINATES.items():
        if st.lower() == state.lower() and dist.lower() == district.lower():
            return c
            
    return None
