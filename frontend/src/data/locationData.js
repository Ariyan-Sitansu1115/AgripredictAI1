/**
 * India location hierarchy: State → District → Local Areas (Taluks/Blocks)
 * Covers all states listed in the app profile form.
 */

export const LOCATION_HIERARCHY = {
  'Andhra Pradesh': {
    'Guntur': ['Guntur', 'Tenali', 'Ponnur', 'Sattenapalle', 'Narasaraopet'],
    'Krishna': ['Vijayawada', 'Machilipatnam', 'Gudivada', 'Nuzvid', 'Tiruvuru'],
    'Kurnool': ['Kurnool', 'Nandyal', 'Adoni', 'Yemmiganur', 'Pattikonda'],
    'East Godavari': ['Rajamahendravaram', 'Kakinada', 'Amalapuram', 'Tuni', 'Pithapuram'],
    'West Godavari': ['Eluru', 'Bhimavaram', 'Tanuku', 'Narasapuram', 'Palakol'],
    'Chittoor': ['Chittoor', 'Tirupati', 'Madanapalle', 'Punganur', 'Piler'],
  },
  'Bihar': {
    'Patna': ['Patna City', 'Danapur', 'Phulwari', 'Masaurhi', 'Bikram'],
    'Gaya': ['Gaya', 'Bodh Gaya', 'Sherghati', 'Nawada', 'Aurangabad'],
    'Muzaffarpur': ['Muzaffarpur', 'Saraiya', 'Kanti', 'Motipur', 'Bochahan'],
    'Bhagalpur': ['Bhagalpur', 'Sultanganj', 'Bihpur', 'Kahalgaon', 'Pirpainti'],
    'Darbhanga': ['Darbhanga', 'Biraul', 'Hayaghat', 'Kiratpur', 'Baheri'],
  },
  'Gujarat': {
    'Ahmedabad': ['Ahmedabad City', 'Sanand', 'Daskroi', 'Dholka', 'Bavla'],
    'Surat': ['Surat City', 'Bardoli', 'Mandvi', 'Olpad', 'Choryasi'],
    'Rajkot': ['Rajkot City', 'Gondal', 'Jetpur', 'Jasdan', 'Kotda Sangani'],
    'Vadodara': ['Vadodara City', 'Padra', 'Dabhoi', 'Karjan', 'Sankheda'],
    'Anand': ['Anand', 'Vallabh Vidyanagar', 'Borsad', 'Petlad', 'Umreth'],
    'Mehsana': ['Mehsana', 'Visnagar', 'Unjha', 'Kadi', 'Kalol'],
  },
  'Haryana': {
    'Ambala': ['Ambala City', 'Ambala Cantt', 'Naraingarh', 'Mullana', 'Shahzadpur'],
    'Hisar': ['Hisar', 'Hansi', 'Barwala', 'Uklana', 'Fatehabad'],
    'Karnal': ['Karnal', 'Panipat', 'Assandh', 'Nilokheri', 'Gharaunda'],
    'Rohtak': ['Rohtak', 'Sampla', 'Kalanaur', 'Asthal Bohar', 'Lakhan Majra'],
    'Sonipat': ['Sonipat', 'Gohana', 'Kharkhoda', 'Rai', 'Ganaur'],
    'Kurukshetra': ['Thanesar', 'Pehowa', 'Ladwa', 'Shahabad', 'Babain'],
  },
  'Karnataka': {
    'Bengaluru Urban': ['Bangalore City', 'Anekal', 'Ramanagara', 'Kanakapura', 'Devanahalli'],
    'Mysuru': ['Mysuru City', 'Nanjangud', 'T. Narsipur', 'Hunsur', 'Periyapatna'],
    'Belagavi': ['Belagavi', 'Gokak', 'Athani', 'Bailhongal', 'Chikkodi'],
    'Dharwad': ['Dharwad', 'Hubli', 'Kalghatgi', 'Navalgund', 'Kundgol'],
    'Shivamogga': ['Shivamogga', 'Bhadravati', 'Sagar', 'Soraba', 'Shikaripura'],
    'Tumakuru': ['Tumakuru', 'Tiptur', 'Gubbi', 'Turuvekere', 'Madhugiri'],
  },
  'Kerala': {
    'Ernakulam': ['Ernakulam City', 'Aluva', 'Angamaly', 'Perumbavoor', 'Kothamangalam'],
    'Thiruvananthapuram': ['Thiruvananthapuram City', 'Nedumangad', 'Attingal', 'Varkala', 'Chirayinkeezhu'],
    'Thrissur': ['Thrissur City', 'Chalakudy', 'Kodungallur', 'Irinjalakuda', 'Kunnamkulam'],
    'Kozhikode': ['Kozhikode City', 'Vadakara', 'Koyilandy', 'Mukkam', 'Perambra'],
    'Palakkad': ['Palakkad', 'Ottapalam', 'Shornur', 'Mannarkkad', 'Chittur'],
  },
  'Madhya Pradesh': {
    'Bhopal': ['Bhopal City', 'Berasia', 'Phanda', 'Huzur', 'Sehore'],
    'Indore': ['Indore City', 'Depalpur', 'Sanwer', 'Mhow', 'Hatod'],
    'Jabalpur': ['Jabalpur City', 'Patan', 'Sihora', 'Katni', 'Bargi'],
    'Gwalior': ['Gwalior City', 'Bhind', 'Datia', 'Shivpuri', 'Morena'],
    'Rewa': ['Rewa', 'Satna', 'Mauganj', 'Teonthar', 'Hanumana'],
    'Ujjain': ['Ujjain', 'Nagda', 'Khachrod', 'Barnagar', 'Tarana'],
  },
  'Maharashtra': {
    'Pune': ['Pune City', 'Pimpri-Chinchwad', 'Haveli', 'Maval', 'Shirur'],
    'Nashik': ['Nashik City', 'Niphad', 'Yeola', 'Sinnar', 'Igatpuri'],
    'Nagpur': ['Nagpur City', 'Kamptee', 'Hingna', 'Narkhed', 'Ramtek'],
    'Aurangabad': ['Aurangabad City', 'Kannad', 'Vaijapur', 'Gangapur', 'Sillod'],
    'Solapur': ['Solapur City', 'Barshi', 'Pandharpur', 'Mangalvedhe', 'Malshiras'],
    'Kolhapur': ['Kolhapur City', 'Karvir', 'Hatkanangale', 'Shirol', 'Panhala'],
  },
  'Odisha': {
    'Khordha': ['Bhubaneswar', 'Khordha', 'Jatani', 'Balianta', 'Begunia'],
    'Cuttack': ['Cuttack City', 'Banki', 'Niali', 'Mahanga', 'Baramba'],
    'Balangir': ['Balangir', 'Titlagarh', 'Patnagarh', 'Kantabanji', 'Saintala'],
    'Puri': ['Puri', 'Nimapara', 'Konark', 'Satyabadi', 'Pipili'],
    'Sambalpur': ['Sambalpur', 'Rengali', 'Kuchinda', 'Bamra', 'Maneswar'],
    'Ganjam': ['Berhampur', 'Bhanjanagar', 'Phulbani', 'Chhatrapur', 'Digapahandi'],
    'Mayurbhanj': ['Baripada', 'Karanjia', 'Bangriposi', 'Jashipur', 'Udala'],
  },
  'Punjab': {
    'Amritsar': ['Amritsar City', 'Ajnala', 'Baba Bakala', 'Majitha', 'Rayya'],
    'Ludhiana': ['Ludhiana City', 'Khanna', 'Jagraon', 'Raikot', 'Payal'],
    'Jalandhar': ['Jalandhar City', 'Adampur', 'Shahkot', 'Nakodar', 'Phillaur'],
    'Patiala': ['Patiala City', 'Rajpura', 'Fatehgarh Sahib', 'Nabha', 'Sangrur'],
    'Bathinda': ['Bathinda City', 'Goniana', 'Talwandi Sabo', 'Mansa', 'Rampura'],
  },
  'Rajasthan': {
    'Jaipur': ['Jaipur City', 'Amber', 'Sanganer', 'Phagi', 'Chaksu'],
    'Jodhpur': ['Jodhpur City', 'Bilara', 'Shergarh', 'Phalodi', 'Bhopalgarh'],
    'Udaipur': ['Udaipur City', 'Vallabhnagar', 'Salumbar', 'Kherwara', 'Mavli'],
    'Ajmer': ['Ajmer City', 'Beawar', 'Nasirabad', 'Kekri', 'Pisangan'],
    'Alwar': ['Alwar City', 'Rajgarh', 'Thanagazi', 'Laxmangarh', 'Tijara'],
    'Kota': ['Kota City', 'Ladpura', 'Ramganj Mandi', 'Sangod', 'Itawa'],
  },
  'Tamil Nadu': {
    'Chennai': ['Chennai North', 'Chennai South', 'Ambattur', 'Alandur', 'Sholinganallur'],
    'Coimbatore': ['Coimbatore City', 'Sulur', 'Kinathukadavu', 'Mettupalayam', 'Pollachi'],
    'Madurai': ['Madurai City', 'Melur', 'Usilampatti', 'Peraiyur', 'Thiruparankundram'],
    'Tiruchirappalli': ['Trichy City', 'Srirangam', 'Musiri', 'Thottiyam', 'Lalgudi'],
    'Salem': ['Salem City', 'Omalur', 'Mettur', 'Yercaud', 'Gangavalli'],
    'Thanjavur': ['Thanjavur', 'Kumbakonam', 'Papanasam', 'Thiruvidaimarudur', 'Orathanadu'],
  },
  'Telangana': {
    'Hyderabad': ['Hyderabad City', 'Secunderabad', 'LB Nagar', 'Uppal', 'Kukatpally'],
    'Warangal': ['Warangal City', 'Parkal', 'Narsampet', 'Mulug', 'Bhupalpally'],
    'Nizamabad': ['Nizamabad City', 'Bodhan', 'Armur', 'Balkonda', 'Kamareddy'],
    'Karimnagar': ['Karimnagar City', 'Huzurabad', 'Jagtial', 'Manthani', 'Sircilla'],
    'Khammam': ['Khammam City', 'Bhadrachalam', 'Kothagudem', 'Palwancha', 'Madhira'],
  },
  'Uttar Pradesh': {
    'Lucknow': ['Lucknow City', 'Bakshi Ka Talab', 'Malihabad', 'Mohanlalganj', 'Gosainganj'],
    'Agra': ['Agra City', 'Firozabad', 'Etah', 'Mainpuri', 'Fatehabad'],
    'Varanasi': ['Varanasi City', 'Gyanpur', 'Ramnagar', 'Pindra', 'Arajiline'],
    'Kanpur': ['Kanpur City', 'Bilhaur', 'Ghatampur', 'Akbarpur', 'Chaubepur'],
    'Allahabad': ['Allahabad City', 'Phulpur', 'Meja', 'Handia', 'Bara'],
    'Meerut': ['Meerut City', 'Hapur', 'Ghaziabad', 'Modinagar', 'Pilkhuwa'],
  },
  'West Bengal': {
    'Kolkata': ['Kolkata City', 'Barrackpore', 'Barasat', 'Dum Dum', 'Salt Lake'],
    'Howrah': ['Howrah City', 'Uluberia', 'Bagnan', 'Shyampur', 'Amta'],
    'Hooghly': ['Chinsurah', 'Serampore', 'Chanditala', 'Arambag', 'Tarakeswar'],
    'Burdwan': ['Burdwan City', 'Asansol', 'Durgapur', 'Memari', 'Kalna'],
    'Midnapore': ['Midnapore City', 'Ghatal', 'Daspur', 'Debra', 'Nandakumar'],
    'Murshidabad': ['Murshidabad', 'Berhampore', 'Lalbagh', 'Kandi', 'Jiaganj'],
  },
};

/**
 * Get districts for a given state
 * @param {string} state
 * @returns {string[]}
 */
export function getDistricts(state) {
  if (!state || !LOCATION_HIERARCHY[state]) return [];
  return Object.keys(LOCATION_HIERARCHY[state]);
}

/**
 * Get local areas for a given state + district
 * @param {string} state
 * @param {string} district
 * @returns {string[]}
 */
export function getLocalAreas(state, district) {
  if (!state || !district) return [];
  const stateData = LOCATION_HIERARCHY[state];
  if (!stateData || !stateData[district]) return [];
  return stateData[district];
}

export const ALL_STATES = Object.keys(LOCATION_HIERARCHY);
