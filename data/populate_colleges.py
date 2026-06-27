import sqlite3
from backend.database.connection import connect_to_database


colleges = [
    ("Indian Institute of Technology Bombay (IIT Bombay)", "STEM", "Mumbai", "Maharashtra", 1, "2,50,000", "JEE Advanced", "23,00,000", "Nandan Nilekani, Manohar Parrikar"),

    ("Indian Institute of Technology Delhi (IIT Delhi)", "STEM", "New Delhi", "Delhi", 2, "2,50,000", "JEE Advanced", "25,00,000", "Raghuram Rajan, Sachin Bansal"),

    ("Indian Institute of Technology Madras (IIT Madras)", "STEM", "Chennai", "Tamil Nadu", 3, "2,40,000", "JEE Advanced", "22,00,000", "Kris Gopalakrishnan, Mahesh Kumar"),

    ("Indian Institute of Technology Kanpur (IIT Kanpur)", "STEM", "Kanpur", "Uttar Pradesh", 4, "2,35,000", "JEE Advanced", "21,00,000", "Ashoke Sen, N. R. Narayana Murthy"),

    ("Indian Institute of Technology Kharagpur (IIT Kharagpur)", "STEM", "Kharagpur", "West Bengal", 5, "2,30,000", "JEE Advanced", "20,00,000", "Arvind Kejriwal, Sundar Pichai"),

    ("Indian Institute of Technology Roorkee (IIT Roorkee)", "STEM", "Roorkee", "Uttarakhand", 6, "2,30,000", "JEE Advanced", "18,50,000", "Vinod Khosla, Ajit Doval"),

    ("Indian Institute of Technology Guwahati (IIT Guwahati)", "STEM", "Guwahati", "Assam", 7, "2,25,000", "JEE Advanced", "17,00,000", "Pawan Goenka, Hitesh Dhingra"),

    ("Indian Institute of Science (IISc Bangalore)", "STEM", "Bengaluru", "Karnataka", 8, "35,000", "JEE Advanced / IAT", "28,00,000", "C. N. R. Rao, Roddam Narasimha"),

    ("Birla Institute of Technology and Science, Pilani (BITS Pilani)", "STEM", "Pilani", "Rajasthan", 9, "5,70,000", "BITSAT", "19,50,000", "Sanjay Mehrotra, Baba Kalyani"),

    ("National Institute of Technology Tiruchirappalli (NIT Trichy)", "STEM", "Tiruchirappalli", "Tamil Nadu", 10, "1,80,000", "JEE Main", "15,50,000", "Shiv Nadar, V. A. Shiva Ayyadurai"),

    ("Delhi Technological University (DTU)", "STEM", "New Delhi", "Delhi", 11, "2,20,000", "JEE Main", "16,00,000", "Vinod Dham, Vijay Shekhar Sharma"),

    ("Vellore Institute of Technology (VIT Vellore)", "STEM", "Vellore", "Tamil Nadu", 12, "2,00,000", "VITEEE", "9,50,000", "G. V. Prakash Kumar, Sai Praneeth"),

    ("International Institute of Information Technology Hyderabad (IIIT Hyderabad)", "STEM", "Hyderabad", "Telangana", 13, "4,50,000", "UGEE / JEE Main", "30,00,000", "Anurag Kumar, Kshitij Marwah"),

    ("Netaji Subhas University of Technology (NSUT)", "STEM", "New Delhi", "Delhi", 14, "2,30,000", "JEE Main", "17,00,000", "Varun Dua, Dinesh Mohan"),

    ("Shri Ram College of Commerce (SRCC)", "Commerce", "New Delhi", "Delhi", 1, "30,000", "CUET UG", "10,50,000", "Arun Jaitley, Gaurav Taneja"),

    ("Lady Shri Ram College for Women (LSR)", "Commerce", "New Delhi", "Delhi", 2, "25,000", "CUET UG", "8,50,000", "Aditi Rao Hydari, Brinda Karat"),

    ("St. Xavier's College, Mumbai (St. Xavier's Mumbai)", "Commerce", "Mumbai", "Maharashtra", 3, "45,000", "Merit-Based", "7,50,000", "Anand Mahindra, Shashi Tharoor"),

    ("Loyola College, Chennai (Loyola College)", "Commerce", "Chennai", "Tamil Nadu", 4, "65,000", "Merit-Based", "6,50,000", "N. Chandrasekaran, S. S. Rajamouli"),

    ("Narsee Monjee College of Commerce and Economics (NM College)", "Commerce", "Mumbai", "Maharashtra", 5, "55,000", "Merit-Based", "8,00,000", "Anil Ambani, Ritesh Agarwal"),

    ("Christ University (Christ)", "Commerce", "Bengaluru", "Karnataka", 6, "2,00,000", "Christ Entrance Test", "7,00,000", "K. L. Rahul, Anil Kumble"),

    ("Shaheed Sukhdev College of Business Studies (SSCBS)", "Commerce", "New Delhi", "Delhi", 7, "35,000", "CUET UG", "11,00,000", "Raghav Chadha, Nitin Gupta"),

    ("Hansraj College", "Commerce", "New Delhi", "Delhi", 8, "25,000", "CUET UG", "8,00,000", "Shah Rukh Khan, Kiren Rijiju"),

    ("Symbiosis College of Arts and Commerce (SCAC)", "Commerce", "Pune", "Maharashtra", 9, "45,000", "Merit-Based", "6,00,000", "Cyrus Broacha, Sushil Kumar Shinde"),

    ("St. Stephen's College", "Humanities", "New Delhi", "Delhi", 1, "45,000", "CUET UG + Interview", "7,00,000", "Shashi Tharoor, Kapil Sibal"),

    ("Miranda House", "Humanities", "New Delhi", "Delhi", 2, "20,000", "CUET UG", "8,50,000", "Brinda Karat, Aditi Rao Hydari"),

    ("Jawaharlal Nehru University (JNU)", "Humanities", "New Delhi", "Delhi", 3, "15,000", "CUET PG", "8,00,000", "S. Jaishankar, Nirmala Sitharaman"),

    ("Ashoka University", "Humanities", "Sonipat", "Haryana", 4, "9,50,000", "Ashoka Aptitude Assessment", "10,00,000", "Aman Gupta, Numerous Rhodes Scholars"),

    ("Tata Institute of Social Sciences (TISS)", "Humanities", "Mumbai", "Maharashtra", 5, "75,000", "CUET PG", "8,50,000", "Harsh Mander, Medha Patkar"),

    ("Jamia Millia Islamia (JMI)", "Humanities", "New Delhi", "Delhi", 6, "18,000", "CUET / JMI Entrance", "7,50,000", "Shah Rukh Khan, Virender Sehwag"),

    ("FLAME University", "Humanities", "Pune", "Maharashtra", 7, "8,00,000", "FLAME Entrance Aptitude Test", "9,00,000", "Karan Bhojwani, Several Startup Founders")
]

def populate_colleges():
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """INSERT INTO CollegeComparision (name, stream, city, state, ranking, annual_fees, entrance_exam, placement_average, notable_alumni)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    for college in colleges:
        cursor.execute(sql,college)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    populate_colleges()