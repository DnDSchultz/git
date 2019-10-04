class Case:
    """ Backend for database query and entry to track the status of Forensic cases."""

    def __init__(self, date_requested, date_completed, case_desc,
                 forensic_only, is_icac, icac_dispo, rep_ofc, forensic_inv):

        self.dr = date_requested  # Format 2019-01-01
        self.dc = date_completed  # Format 2019-01-01
        self.cd = case_desc  # Short description
        self.fo = forensic_only  # y or n
        self.ii = is_icac  # y or n
        self.id = icac_dispo  #IDS Updated y or n or na
        self.ro = rep_ofc  # Last name
        self.fi = forensic_inv  # Last name

ea19001234 = Case("dr","dc","cd","fo","ii","id","ro","fi")

print(ea19001234.cd)
