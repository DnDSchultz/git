class Case:
    """ Backend for database query and entry to track the status of Forensic cases."""

    def __init__(self, case_num, date_requested, date_completed, case_desc,
                 forensic_only, is_icac, icac_dispo, rep_ofc, forensic_inv):
        self.cn = case_num #8 didget
        self.dr = date_requested  # Format 2019-01-01
        self.dc = date_completed  # Format 2019-01-01
        self.cd = case_desc  # Short description
        self.fo = forensic_only  # y or n
        self.ii = is_icac  # y or n
        self.id = icac_dispo  #IDS Updated y or n or na
        self.ro = rep_ofc  # Last name
        self.fi = forensic_inv  # Last name


case_num = ("19001234")
date_requested = "2018-06-01"
case_desc = "Test case description"
forensic_inv = "Null"


case = Case(case_num,date_requested,None,case_desc,None,None,None,None,forensic_inv)

li = ("ea" + case.cn)

print(li)
