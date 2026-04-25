// Real cuts from bremen_merged_final.csv (1,083 companies, >10 employees, Bremen DE)
window.DDE_DATA = {
  meta: {
    n: 1083,
    nScalers: 128,
    overallRate: 11.82,
    nGazelles: 5,
    course: "Data-Driven Entrepreneurship",
    school: "WHU – Otto Beisheim School of Management",
    term: "Spring 2026",
    region: "Bremen, Germany",
    employeeFilter: ">10 employees",
    horizon: "2019 – 2024",
  },

  // Sector — top + bottom; rate %, n
  sectors: [
    { code: "I", name: "Hospitality", n: 40, rate: 32.5 },
    { code: "P", name: "Education", n: 11, rate: 27.3 },
    { code: "R", name: "Arts & recreation", n: 12, rate: 25.0 },
    { code: "J", name: "Information & comms", n: 58, rate: 17.2 },
    { code: "E", name: "Water & waste", n: 25, rate: 16.0 },
    { code: "L", name: "Real estate", n: 28, rate: 14.3 },
    { code: "H", name: "Transport & storage", n: 111, rate: 13.5 },
    { code: "F", name: "Construction", n: 76, rate: 13.2 },
    { code: "C", name: "Manufacturing", n: 109, rate: 12.8 },
    { code: "M", name: "Prof. services", n: 156, rate: 12.2 },
    { code: "N", name: "Admin services", n: 88, rate: 8.0 },
    { code: "G", name: "Wholesale & retail", n: 217, rate: 7.8 },
    { code: "K", name: "Finance & insurance", n: 28, rate: 7.1 },
    { code: "Q", name: "Health & social", n: 76, rate: 6.6 },
    { code: "S", name: "Other services", n: 37, rate: 2.7 },
  ],

  legalForm: [
    { k: "AG", n: 11, rate: 18.2 },
    { k: "GmbH", n: 612, rate: 14.4 },
    { k: "Other", n: 181, rate: 9.9 },
    { k: "GmbH & Co. KG", n: 166, rate: 9.6 },
    { k: "e.V.", n: 24, rate: 8.3 },
    { k: "KG", n: 31, rate: 3.2 },
  ],

  b2b: [
    { k: "B2B", n: 393, rate: 12.2 },
    { k: "Both", n: 156, rate: 10.9 },
    { k: "B2C", n: 104, rate: 6.7 },
  ],

  age: [
    { k: "0–10 yrs", n: 198, rate: 18.2 },
    { k: "10–25 yrs", n: 460, rate: 13.9 },
    { k: "25–50 yrs", n: 276, rate: 7.6 },
    { k: "50–100 yrs", n: 120, rate: 5.0 },
    { k: "100+ yrs", n: 28, rate: 3.6 },
  ],

  size: [
    { k: "11–24", n: 489, rate: 7.0 },
    { k: "25–49", n: 239, rate: 16.7 },
    { k: "50–99", n: 152, rate: 13.8 },
    { k: "100–249", n: 123, rate: 16.3 },
    { k: "250–499", n: 43, rate: 16.3 },
    { k: "500+", n: 37, rate: 16.2 },
  ],

  topScalers: [
    { name: "Nordsee Nassbagger- und Tiefbau", legal: "GmbH", industry: "Marine construction", aagr: 57.3, emp: 74 },
    { name: "Bewo Telehealthcare", legal: "GmbH", industry: "Telehealth", aagr: 56.7, emp: 50 },
    { name: "Monacor International", legal: "GmbH & Co. KG", industry: "Pro audio", aagr: 55.6, emp: 128 },
    { name: "Mirac Großhandel", legal: "GmbH", industry: "Poultry wholesale", aagr: 50.6, emp: 41 },
    { name: "Theramobile", legal: "Other", industry: "Mobility / e-trikes", aagr: 47.4, emp: 32 },
    { name: "Fitness-Park am Becketal", legal: "GmbH", industry: "Fitness", aagr: 43.6, emp: 74 },
    { name: "DGS", legal: "Other", industry: "Event tech", aagr: 35.7, emp: 25 },
    { name: "BSB Erwachsenenbildung", legal: "GmbH", industry: "Adult education", aagr: 35.2, emp: 42 },
    { name: "Kocks Manufacturing", legal: "GmbH & Co. KG", industry: "Mech. engineering", aagr: 34.8, emp: 98 },
  ],

  // Definition language
  defs: {
    scaler: "Avg. annualised employment growth ≥ 10% over a 5-year window, base ≥ 10 staff (OECD)",
    gazelle: "≥ 20% AAGR over 3 years, base ≥ 10 staff",
  },
};
