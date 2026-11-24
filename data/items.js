/* 體檢項目解說資料 — 按項目分類，每項可展開說明 */
window.ITEMS_DATA = [
  {
    "id": "blood",
    "name": "血液檢查",
    "en": "BLOOD TESTS",
    "icon": "drop",
    "intro": "從少量血液了解身體基本狀況，包括血細胞、電解質、血糖及血脂。",
    "items": [
      { "name": "血全圖", "en": "Complete Blood Picture / Count (CBP, CBC)", "desc": "計算紅血球、白血球、血小板等項目，用來了解有沒有貧血、感染跡象或血小板異常。各項數值需由醫護人員按個人情況解讀。" },
      { "name": "血紅素", "en": "Haemoglobin", "desc": "反映血液輸送氧氣的能力。數值偏低可能與貧血有關，偏高亦可能與其他身體狀況有關。" },
      { "name": "紅血球計數", "en": "Red Blood Cell Count (RBC)", "desc": "計算血液中紅血球的數量，配合血紅素及血球壓積量，用來評估貧血或紅血球相關問題。" },
      { "name": "白血球計數", "en": "White Blood Cell Count (WBC)", "desc": "白血球與身體防禦功能有關。數量變化可反映身體正在應付感染、炎症或其他情況。" },
      { "name": "血小板計數", "en": "Platelet Count", "desc": "血小板參與止血。數量過低或過高都值得留意，需由醫護人員進一步評估。" },
      { "name": "血球壓積量", "en": "Haematocrit (PCV / HCT)", "desc": "量度紅血球佔血液的比例，是評估貧血及血液濃稠程度的常用指標。" },
      { "name": "血球形態分析", "en": "Peripheral Blood Smear", "desc": "在顯微鏡下觀察血球形狀，提供一些自動化計數未能顯示的線索。" },
      { "name": "血沉降率", "en": "Erythrocyte Sedimentation Rate (ESR)", "desc": "觀察紅血球沉澱速度，是一項較籠統的炎症相關指標，需要與其他檢查一併看。" },
      { "name": "血糖", "en": "Glucose (Fasting / Random)", "desc": "量度血液中的葡萄糖水平，用來了解血糖控制情況。空腹與餐後量度的意義不同。" },
      { "name": "糖化血色素", "en": "Glyco-Hb (HbA1c)", "desc": "反映過去約兩至三個月的平均血糖水平，較單次血糖測試更能顯示長期情況。" },
      { "name": "葡萄糖耐量測試", "en": "Glucose Tolerance Test", "desc": "飲用含糖溶液後在指定時間量度血糖，用來觀察身體處理糖分的能力。" },
      { "name": "總膽固醇", "en": "Cholesterol, Total", "desc": "血液中所有膽固醇的總和，是評估心血管風險的其中一項數據。" },
      { "name": "高密度膽固醇", "en": "Cholesterol HDL", "desc": "一般稱為「好膽固醇」，數值與心血管健康狀況有關。" },
      { "name": "低密度膽固醇", "en": "Cholesterol LDL (Direct)", "desc": "一般稱為「壞膽固醇」，數值偏高時通常建議檢視飲食及生活習慣。" },
      { "name": "三酸甘油脂", "en": "Triglycerides", "desc": "血液中的脂肪之一，與飲食、體重及代謝情況有關。" },
      { "name": "鈉", "en": "Sodium", "desc": "電解質之一，與體液平衡及血壓有關。過高或過低都需要查找原因。" },
      { "name": "鉀", "en": "Potassium", "desc": "電解質之一，與心臟及肌肉功能有關。異常數值需要及时处理。" },
      { "name": "氯化物", "en": "Chloride", "desc": "電解質之一，與體液及酸鹼平衡有關，通常與其他電解質一併解讀。" },
      { "name": "鈣", "en": "Calcium", "desc": "與骨骼、牙齒、神經及肌肉功能有關。數值異常可能與多種身體狀況有關。" },
      { "name": "同型半胱胺酸", "en": "Homocysteine", "desc": "與心血管風險及某些營養素狀態有關的一項指標。" }
    ]
  },
  {
    "id": "liver",
    "name": "肝腎功能",
    "en": "LIVER & RENAL FUNCTION",
    "icon": "shield",
    "intro": "了解肝臟代謝、膽汁分泌及腎臟過濾功能，是體檢中常見的基礎組合。",
    "items": [
      { "name": "谷丙轉氨酶", "en": "SGPT (ALT)", "desc": "主要存在於肝細胞，數值上升時通常提示肝細胞受到刺激或損害。" },
      { "name": "谷草轉氨酶", "en": "SGOT (AST)", "desc": "存在於肝臟、肌肉等多種組織，需與其他肝功能項目一併解讀。" },
      { "name": "鹼性磷酸酶", "en": "Alkaline Phosphatase (ALP)", "desc": "與肝臟及骨骼有關，數值變化可提供一些膽道或骨骼方面的線索。" },
      { "name": "丙種谷氨酰轉肽酶", "en": "Gamma Glutamyl Transferase (GGT)", "desc": "與肝臟及膽道有關，常用於配合其他肝功能項目作判斷。" },
      { "name": "總膽紅素", "en": "Bilirubin, Total", "desc": "膽紅素是血紅素分解後的產物，數值可反映肝臟處理及排泄膽紅素的情況。" },
      { "name": "直接膽紅素", "en": "Bilirubin, Direct", "desc": "經肝臟處理後的膽紅素，與總膽紅素一起看可帮助分辨不同情況。" },
      { "name": "總蛋白", "en": "Protein, Total", "desc": "血漿中各類蛋白質的總量，與營養狀態、肝臟及免疫情況有關。" },
      { "name": "白蛋白", "en": "Albumin", "desc": "由肝臟製造的蛋白質，與營養狀態及體液平衡有關。" },
      { "name": "球蛋白", "en": "Globulin", "desc": "包含多種與免疫有關的蛋白質，與白蛋白一起可計算比例。" },
      { "name": "白蛋白球蛋白比例", "en": "A/G Ratio", "desc": "白蛋白與球蛋白的比例，可提供一些肝臟或免疫方面的線索。" },
      { "name": "肌酸酐", "en": "Creatinine", "desc": "肌肉代謝產物，主要經腎臟排出，是評估腎臟過濾功能的常用指標。" },
      { "name": "尿素", "en": "Urea / BUN", "desc": "蛋白質代謝後的產物，經腎臟排出，數值受腎功能、水分及飲食影響。" },
      { "name": "尿酸", "en": "Uric Acid", "desc": "嘌呤代謝的最終產物，數值偏高與痛風及代謝情況有關。" },
      { "name": "重碳酸鹽", "en": "Bicarbonate (HCO3)", "desc": "與身體酸鹼平衡有關的電解質，通常與其他電解質一併解讀。" },
      { "name": "肌酸酐清除試驗", "en": "Creatinine Clearance Test", "desc": "結合血液及尿液數據，用來估算腎臟每分鐘過濾血液的能力。" }
    ]
  },
  {
    "id": "infection",
    "name": "感染及病理",
    "en": "DISEASE / INFECTION",
    "icon": "scan",
    "intro": "針對細菌、病毒及寄生蟲等感染相關檢查，以及身體發炎情况的指標。",
    "items": [
      { "name": "乙型肝炎表面抗原", "en": "Hepatitis B Surface Antigen (HBsAg)", "desc": "用來檢測體內是否帶有乙型肝炎表面抗原，是乙肝篩查的基本項目之一。" },
      { "name": "乙型肝炎表面抗體", "en": "Hepatitis B Surface Antibody (HBsAb)", "desc": "反映身體對乙型肝炎是否有免疫保護，接種疫苗後常會檢查此項。" },
      { "name": "乙型肝炎核心抗體", "en": "Hepatitis B Core Antibody (HBcAb)", "desc": "用於了解曾否接觸過乙型肝炎病毒，需配合其他乙肝項目解讀。" },
      { "name": "丙型肝炎抗體", "en": "Hepatitis C Virus Antibody (HCV-Ab)", "desc": "用來篩查是否曾接觸丙型肝炎病毒，陽性結果需要進一步檢查。" },
      { "name": "甲型肝炎抗體", "en": "Hepatitis A Virus Antibody (HAV-IgG / IgM)", "desc": "分辨過往感染或近期感染的甲型肝炎抗體，IgM 一般與急性感染有關。" },
      { "name": "愛滋病毒抗體", "en": "HIV I & II Antibody", "desc": "用來篩查是否曾接觸愛滋病毒。任何異常結果都應由醫護人員安排進一步跟進。" },
      { "name": "梅毒血清試驗", "en": "VDRL / RPR", "desc": "梅毒篩查常用的血清測試，需配合其他測試一起解讀。" },
      { "name": "幽門螺旋桿菌抗體", "en": "Helicobacter pylori Antibody IgG", "desc": "用來了解是否曾接觸幽門螺旋桿菌，與胃部不適及潰瘍風險有關。" },
      { "name": "C13 幽門螺旋桿菌吹氣測試", "en": "C13 Urea Breath Test", "desc": "飲用特定溶液後吹氣，用來檢查胃內是否有幽門螺旋桿菌，屬非侵入性測試。" },
      { "name": "鼻咽癌病毒抗體", "en": "Epstein Barr Virus Antibody (EBV)", "desc": "與鼻咽癌風險評估有關的病毒抗體項目，需由醫護人員按個人情況解讀。" },
      { "name": "類風濕關節炎因子", "en": "Rheumatoid Arthritis Factor (RA Factor)", "desc": "與類風濕關節炎等自身免疫情況有關的指標，不能單獨作為判斷依據。" },
      { "name": "丙種反應蛋白", "en": "C-Reactive Protein (CRP)", "desc": "身體發炎時會上升的蛋白質，用來觀察炎症活動情況。" },
      { "name": "抗核抗體", "en": "Anti-Nuclear Factor (ANF)", "desc": "與自身免疫疾病相關的篩查項目，需配合症狀及其他檢查解讀。" },
      { "name": "血型", "en": "ABO Grouping / Rh (D)", "desc": "確認 ABO 血型及 Rh 因子，是輸血、懷孕檢查及一般健康資料的一部分。" },
      { "name": "德國麻疹抗體", "en": "Rubella Antibody IgG / IgM", "desc": "用來了解對德國麻疹的免疫情況，IgM 與近期感染有關。" }
    ]
  },
  {
    "id": "markers",
    "name": "癌症指標及荷爾蒙",
    "en": "TUMOUR MARKERS & HORMONES",
    "icon": "heart",
    "intro": "癌症指標與荷爾蒙項目需要配合影像、病史及其他檢查，由醫護人員綜合解讀。",
    "items": [
      { "name": "甲種胎兒蛋白", "en": "Alpha Fetoprotein (AFP)", "desc": "常用於肝臟相關的健康篩查，數值異常需要配合影像檢查跟進。" },
      { "name": "癌胚抗原", "en": "Carcinoembryonic Antigen (CEA)", "desc": "與胃腸道等部位有關的癌症指標，常用於跟進已知情況而非單獨篩查。" },
      { "name": "癌抗原 15.3", "en": "CA 15.3", "desc": "與乳房組織有關的癌症指標，多用於跟進而非一般篩查。" },
      { "name": "癌抗原 19.9", "en": "CA 19.9", "desc": "與胰臟及膽道等部位有關的癌症指標，需配合其他檢查解讀。" },
      { "name": "癌抗原 125", "en": "CA 125", "desc": "與卵巢等部位有關的癌症指標，良性情況亦可能令數值上升。" },
      { "name": "前列腺癌抗原", "en": "Prostate Specific Antigen (PSA)", "desc": "與前列腺有關的指標，前列腺增生或炎症亦可能令數值上升。" },
      { "name": "人絨毛膜促性腺激素", "en": "Beta-HCG", "desc": "與懷孕情况及某些腫瘤相關的指標，需按檢查目的解讀。" },
      { "name": "鱗狀細胞癌抗原", "en": "Squamous Cell Carcinoma Antigen (SCC)", "desc": "與鱗狀細胞癌相關的指標，需配合其他檢查綜合判斷。" },
      { "name": "促甲狀腺激素", "en": "Thyroid Stimulating Hormone (TSH)", "desc": "反映甲狀腺功能的重要指標，過高或過低都可能有不同意義。" },
      { "name": "遊離亞甲狀腺素", "en": "Free T4 (FT4)", "desc": "甲狀腺激素的一種，與 TSH 一起判讀可了解甲狀腺功能狀態。" },
      { "name": "遊離三碘甲狀腺原氨酸", "en": "Free T3 (FT3)", "desc": "另一種甲狀腺激素，通常在甲狀腺功能異常時提供更多資料。" },
      { "name": "皮質醇", "en": "Cortisol", "desc": "與壓力反應及新陳代謝有關的荷爾蒙，量度時間會影響結果。" },
      { "name": "雌二醇", "en": "Estradiol (E2)", "desc": "女性主要雌激素之一，與月經週期及生殖健康有關。" },
      { "name": "孕酮", "en": "Progesterone", "desc": "與月經週期及懷孕有關的荷爾蒙，需按檢查時間點解讀。" },
      { "name": "睪固酮", "en": "Testosterone", "desc": "與男性生殖健康、肌肉及骨骼等有關的荷爾蒙。" }
    ]
  },
  {
    "id": "imaging",
    "name": "影像檢查",
    "en": "IMAGING",
    "icon": "scan",
    "intro": "利用超聲波、X 光、磁力共振及電腦掃描等技術，直接觀察身體結構。",
    "items": [
      { "name": "腹部超聲波", "en": "Ultrasound – Whole / Upper Abdomen", "desc": "用高頻聲波觀察肝、膽、脾、胰、腎等器官，檢查前通常需要禁食。" },
      { "name": "骨盆超聲波", "en": "Ultrasound – Pelvis", "desc": "觀察子宮、卵巢等盆腔器官，部分情況需要預先飲水令膀胱脹滿。" },
      { "name": "前列腺超聲波", "en": "Ultrasound – Prostate", "desc": "經腹部觀察前列腺大小及結構，通常亦需要脹膀胱配合。" },
      { "name": "頸動脈超聲波", "en": "Carotid Ultrasound", "desc": "觀察頸部血管有沒有狹窄或斑塊，與中風風險評估有關。" },
      { "name": "乳房造影", "en": "Mammography", "desc": "使用低劑量 X 光拍攝乳房影像，是乳房健康篩查的常見方法。" },
      { "name": "X 光胸部平片", "en": "Chest X-Ray", "desc": "觀察肺部、心臟及胸廓的大致情況，常用於入職或基本健康檢查。" },
      { "name": "雙源電腦掃描", "en": "Dual Source CT Scan", "desc": "利用 X 光斷層掃描身體結構，部分心臟血管檢查需要特別準備。" },
      { "name": "磁力共振影像掃描 1.5T", "en": "Magnetic Resonance Imaging 1.5T (MRI)", "desc": "利用磁場及無線電波產生影像，適合觀察軟組織。體內有金屬植入物者須先告知醫護。" },
      { "name": "站立式全身 X 光", "en": "EOS Imaging System", "desc": "以較低輻射劑量拍攝站立姿勢的全身影像，常用於骨骼及姿勢評估。" },
      { "name": "無創肝臟檢測", "en": "FibroScan", "desc": "以即時彈性成像技術量度肝臟硬度及脂肪量，過程無需穿刺。" },
      { "name": "靜態心電圖", "en": "Resting ECG", "desc": "記錄心臟電活動，用來觀察心律及心跳是否正常。" },
      { "name": "24 小時血壓測試", "en": "24 Hour Blood Pressure Test", "desc": "在日常生活下連續記錄血壓，較單次量度更能反映全日情況。" },
      { "name": "骨質密度掃描", "en": "DEXA Bone Density Scan", "desc": "量度骨骼礦物密度，用來評估骨質疏鬆風險。" }
    ]
  },
  {
    "id": "urine",
    "name": "尿液檢查",
    "en": "URINE TESTS",
    "icon": "drop",
    "intro": "尿液檢查能反映腎臟、泌尿系統及部分代謝情況，收集方法會影響結果。",
    "items": [
      { "name": "小便常規", "en": "Routine Examination (Urine)", "desc": "檢查尿液顏色、比重、糖、蛋白、血細胞等基本項目，是體檢常見組合。" },
      { "name": "小便細菌培養及藥物敏感", "en": "Urine Culture & Sensitivity Test", "desc": "培養尿液中的細菌並測試適合的藥物，用於跟進泌尿系統感染。" },
      { "name": "微白蛋白／肌酸酐比值", "en": "Microalbumin / Creatinine Ratio", "desc": "用來觀察尿液中的微量白蛋白，與早期腎臟變化及糖尿病跟進有關。" },
      { "name": "尿糖", "en": "Urine Glucose", "desc": "尿液中的糖分，數值異常時通常需要配合血糖檢查。" },
      { "name": "妊娠試驗", "en": "Pregnancy Test (Urine)", "desc": "檢測尿液中的懷孕相關荷爾蒙，作懷孕篩查之用。" },
      { "name": "尿液滲透壓", "en": "Urine Osmolality", "desc": "反映尿液濃稀程度，與身體水分及腎臟濃縮功能有關。" },
      { "name": "尿液電解質", "en": "Urine Sodium / Potassium / Chloride", "desc": "量度尿液中的電解質，協助評估腎臟及體液平衡情況。" }
    ]
  },
  {
    "id": "stool",
    "name": "大便及微生物",
    "en": "STOOL TESTS & MICROBIOLOGY",
    "icon": "lab",
    "intro": "涵蓋大便常規、隱血、寄生蟲及細菌培養等項目，與腸胃及感染評估有關。",
    "items": [
      { "name": "大便常規", "en": "Stool Routine", "desc": "觀察大便性狀、顏色、隱血、寄生蟲卵等基本項目，反映腸胃道狀況。" },
      { "name": "大便隱血", "en": "Stool Occult Blood", "desc": "檢測肉眼看不見的少量血液，是腸胃道健康篩查的常見項目。" },
      { "name": "幽門螺旋桿菌大便測試", "en": "Stool for H. pylori Antigen Test", "desc": "從大便樣本檢測幽門螺旋桿菌抗原，作胃部感染篩查。" },
      { "name": "梨形蟲", "en": "Giardia", "desc": "檢測大便中是否帶有梨形蟲，與腸胃不適及寄生蟲感染有關。" },
      { "name": "蟯蟲檢查", "en": "Cellulose Tape Exam for Pinworm", "desc": "以透明膠帶採樣檢查蟯蟲，常用於兒童腸道寄生蟲篩查。" },
      { "name": "細菌培養及藥物敏感試驗", "en": "Culture & Sensitivity Test", "desc": "培養樣本中的細菌並測試藥物反應，協助醫護選擇合適治療。" },
      { "name": "革蘭氏染色塗片", "en": "Gram Stain", "desc": "快速觀察樣本中細菌的類型，為感染評估提供初步資料。" },
      { "name": "結核桿菌塗片", "en": "A.F.B. Smear", "desc": "在顯微鏡下尋找抗酸桿菌，是肺結核等檢查的其中一環。" }
    ]
  },
  {
    "id": "other",
    "name": "其他檢查",
    "en": "OTHER TESTS",
    "icon": "lab",
    "intro": "包括病理、精液分析、結石分析及生活方式相關檢測等項目。",
    "items": [
      { "name": "柏氏抹片", "en": "Pap Smear", "desc": "採集子宮頸細胞作顯微鏡檢查，是女性子宮頸健康篩查的常用方法。" },
      { "name": "病理活組織檢驗", "en": "Biopsy / Section", "desc": "取出少量組織作顯微鏡檢查，由病理專科提供詳細資料。" },
      { "name": "精液分析", "en": "Seminal Fluid Analysis", "desc": "分析精液量、精子數量及活動力等，與生育評估有關。" },
      { "name": "結石成份分析", "en": "Stone Analysis", "desc": "分析結石的化學成份，協助了解形成原因及日後預防方向。" },
      { "name": "酒精測試", "en": "Alcohol", "desc": "量度血液中酒精濃度，結果受飲酒時間及身體代謝影響。" },
      { "name": "鉛", "en": "Lead", "desc": "環境接觸相關的重金屬項目，過量暴露可能影響健康。" },
      { "name": "維生素 B-12", "en": "Vitamin B-12", "desc": "與神經系統及紅血球製造有關的營養素，偏低可能與貧血有關。" },
      { "name": "葉酸", "en": "Folate (Folic acid)", "desc": "與紅血球製造及胎兒發育有關的營養素，備孕及懷孕期間尤其重要。" },
      { "name": "鐵質及總鐵結合量", "en": "Iron & TIBC", "desc": "兩項一起看可反映身體鐵質儲存及輸送情況，常用於貧血評估。" }
    ]
  }
];
