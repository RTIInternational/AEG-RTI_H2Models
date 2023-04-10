Option Explicit
Private CalculateNow As Boolean
Private OldTable As String  'if a new table has been selected, then allow recalculation of values
Private OldType As String 'if a new type has been selected, allow recalculation
Private NewColor As New clsCellColors

Sub ProjInfo()
    'link to the Project Information sheet
    Worksheets("Title").Activate
    ActiveSheet.Range("$A$1").Select
End Sub
Sub InputSheet()
    Worksheets("Input_Sheet_Template").Activate
End Sub
Sub ShowKey()
    ColorKey.Show
End Sub
Sub UseDefaultValues()
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    
    Call UseDefaults("Input_Value_Defaults")
    
    Application.ScreenUpdating = True
    Application.EnableEvents = True
End Sub

Sub UseDefaultValuesCO2()
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    
    Call UseDefaults("CO2_Value_Defaults")
    
    Application.ScreenUpdating = True
    Application.EnableEvents = True
End Sub
Sub EnterPrice()
 
If ActiveSheet.Shapes("Rounded Rectangle 47").Fill.ForeColor.RGB = RGB(128, 128, 225) Then
       ActiveSheet.Shapes("Rounded Rectangle 47").Fill.ForeColor.RGB = RGB(255, 204, 153)
       ActiveSheet.Shapes("Rounded Rectangle 47").TextFrame.Characters.Text = "Enter Cost Manually"
        ActiveSheet.Shapes("Rounded Rectangle 47").TextFrame.Characters.Font.Color = RGB(0, 0, 0)


   
        'lblUseDfltPrice.Visible = True
        Application.Goto reference:="TMP_Escalation"
        Selection.Value = "yes"
        Application.Goto reference:="TMP_StartPrice"
         'insert the price lookup equation
        Application.Range("TMP_StartPrice").Formula = "=HLOOKUP(startup_year,INDIRECT(TMP_PriceTable),MATCH(TMP_FeedName,INDIRECT(Energy_Feed_List),0),FALSE)*TMP_Conversion"
        Call CalculatedCell


ElseIf ActiveSheet.Shapes("Rounded Rectangle 47").Fill.ForeColor.RGB = RGB(255, 204, 153) Then
   ActiveSheet.Shapes("Rounded Rectangle 47").Fill.ForeColor.RGB = RGB(128, 128, 225)
   ActiveSheet.Shapes("Rounded Rectangle 47").TextFrame.Characters.Text = "Use Cost Tables"
   ActiveSheet.Shapes("Rounded Rectangle 47").TextFrame.Characters.Font.Color = RGB(255, 255, 255)

    
    
         Application.Range("TMP_Escalation").Value = "no"
        'lblUseDfltPrice.Visible = False
        Application.Goto reference:="TMP_StartPrice"
        Call InputCell
    
    
    
End If

End Sub




Sub Delete()
        Toolkit_Control_Panel.Show vbModal
End Sub
Sub Add()
'insert new rows and add the new material to the input list
    Dim FeedType As String
    Dim InsertLocName As String
    Dim InsertLocRow As Long
    Dim InsertRowsTxt As String 'lazy lazy lazy
    Dim FeedUse As Double 'the amount used/kg H2 = TMP_Usage
    
    '****************************error handling***************************
    'On Error GoTo ErrHandler
    If Working = True Then Exit Sub
    'if the input sheet is not the active sheet, exit the sub
    If ActiveSheet.Name <> "Input_Sheet_Template" Then Exit Sub
    'get the values for the variables
    FeedUse = Application.Evaluate("TMP_Usage").Value
    If FeedUse = 0 Then
        MsgBox "Please enter a value for the usage"
        Exit Sub
    End If
    '****************************error handling***************************
    
    FeedType = CStr(Application.Evaluate("TMP_FeedType").Value)
    Select Case FeedType
        Case "feedstock"
            InsertLocName = "START_FEED"
        Case "utility"
            InsertLocName = "START_UTILITY"
        Case "byproduct"
            InsertLocName = "START_BYPROD"
        Case Else
            InsertLocName = "STOP"
    End Select
    If InsertLocName = "STOP" Then Exit Sub
    'link the values to the appropriate named ranges
    Application.Goto reference:=InsertLocName
    InsertLocRow = Selection.Row
    InsertRowsTxt = CStr(InsertLocRow) & ":" & CStr(InsertLocRow + 1)
    Rows(InsertRowsTxt).Select
    Selection.Insert Shift:=xlDown
    
    Range("VAR_FEED_VALUES").Select
    Selection.Copy
    Cells(InsertLocRow, 2).Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=True
        
    '*************************call the sub for yearly prices here*************************
    '*************************************************************************************
    'first define the locations for the cells that will be referenced
    Dim FeedNameCell As Range
    Dim ConversionCell As Range
    Dim UsageCell As Range
    Dim LookupCell As Range
    Dim PriceCell As Range
    Dim NewVarName As String
    Dim NewuVarName As String
    Dim NewTxtName As String
    Dim NewuTxtName As String
    Dim SpaceforCost As Boolean
    
    Set FeedNameCell = Cells(InsertLocRow + 1, 2)
    Set ConversionCell = Cells(InsertLocRow + 1, 3)
    Set UsageCell = Cells(InsertLocRow + 1, 5)
    Set LookupCell = Cells(InsertLocRow + 1, 7)
    Set PriceCell = Cells(InsertLocRow + 1, 4)
    
    NewuVarName = AssignSensitivityNames(FeedType, FeedNameCell, UsageCell, "_Usage")
    NewuTxtName = FeedType & " " & CStr(FeedNameCell.Value) & " Usage"
    
    NewVarName = AssignSensitivityNames(FeedType, FeedNameCell, PriceCell, "_Price")
    NewTxtName = FeedType & " " & CStr(FeedNameCell.Value) & " Price"
    
    'Hook up the cash flow sheet and the input sheet
    SpaceforCost = FeedstockYearlyCost(FeedType, FeedNameCell, ConversionCell, UsageCell, LookupCell, PriceCell, NewuVarName, NewVarName)
    If SpaceforCost = False Then
        MsgBox "Only four feed, utility or byproduct values may be added"
        Worksheets("Input_Sheet_Template").Activate
        Application.Goto reference:="START_TOP"
        Exit Sub
    End If
    
    'Add the text names and new variable names to the sensitivity analysis list
    'always add the usage values
    Call AddtoSensList(NewuTxtName, NewuVarName)
    'only add the price if the user has entered their own price
    If CStr(LookupCell.Value) = "no" Then
        Call AddtoSensList(NewTxtName, NewVarName)
    End If
    
    'activate the input sheet
    Worksheets("Input_Sheet_Template").Activate
    
    Application.Goto reference:="START_TOP"

    Exit Sub
ErrHandler:
    MsgBox "Error in cmdAddMaterial event"
End Sub
Sub ViewDescription()
    'link to the Project Information sheet
    Worksheets("Description").Activate
    ActiveSheet.Range("$A$1").Select
End Sub
Sub ViewEdit()
    'view or change original design capital cost estimate
    Worksheets("Capital Costs").Activate
    ActiveSheet.Range("$A$1").Select

End Sub
Sub LinkToDetailedSheet()
    'link or unlink the CO2_seq cells on the input sheet to the detail cost sheet
    'If cmdLinkCO2.Caption = "Link to Detail Sheet" Then 'link the sheets
    If ActiveSheet.Shapes("Rounded Rectangle 56").TextFrame.Characters.Text = "Link to Detail Sheet" Then
        'link the CO2 sequestration cells and make the cells blue (calculated)
        Application.Range("CO2_seq").Formula = "=" & "Det_CO2_seq"
        NewColor.clsCalcCell ("CO2_seq")
        Application.Range("CO2_OandMcost").Formula = "=" & "Det_CO2_OandMcost"
        NewColor.clsCalcCell ("CO2_OandMcost")

        Application.Range("CO2_CashFlow_eUse").Cells(1, 1).Value = "= CO2_eUse_kWhpkg"
        'make the CCS results visible
        Application.Range("Tbl_Result_CCSCost").Cells.Interior.ColorIndex = 2
        'then go to the carbon sequestration page
        Worksheets("Carbon Sequestration").Activate
        Application.Range("CO2_inuse").Cells(1, 1).Value = "Carbon Sequestration"
        NewColor.clsInputCell ("DR_Carbon_Sequestration_2") 'CCS cost inputs
        NewColor.clsInputCell ("DR_Carbon_Sequestration_1") 'CCS cost inputs
        'fill in the default values
        Call UseDefaults("CO2_Value_Defaults")
        'change the caption to "unlink"
        'ActiveSheet.Shapes("Rounded Rectangle 56").TextFrame.Characters.Text = "Unlink"
        Sheets("Input_Sheet_Template").Shapes("Rounded Rectangle 56").TextFrame.Characters.Text = "Unlink"
        
    Else 'unlink the sheets
        'unlink the CO2 sequestration cells and make the cells orange (input)
        Application.Range("CO2_seq").Formula = ""
        NewColor.clsInputCell ("CO2_seq")
        Application.Range("CO2_OandMcost").Formula = ""
        NewColor.clsInputCell ("CO2_OandMcost")

        Application.Range("CO2_CashFlow_eUse").Cells(1, 1).Value = ""
        'make the CCS results not visible (gray)
        Application.Range("Tbl_Result_CCSCost").Cells.Interior.ColorIndex = 15

        Application.Range("CO2_inuse").Cells(1, 1).Value = "To Use Carbon Sequestration Click 'Link to Detail Sheet' in the Input Sheet Capital Cost Section"
        NewColor.clsDisabledCell ("DR_Carbon_Sequestration_2") 'CCS cost inputs
        NewColor.clsDisabledCell ("DR_Carbon_Sequestration_1") 'CCS cost inputs
        'change the caption to "link"
        ActiveSheet.Shapes("Rounded Rectangle 56").TextFrame.Characters.Text = "Link to Detail Sheet"

    End If
End Sub
Sub EnterPrices2()
'The default is to use the H2A price, which is false for this toggle button.
'first, make the cell look like an input cell

    '****************************error handling***************************
    On Error GoTo ErrHandler
    'if the input sheet is not the active sheet, exit the sub
    If ActiveSheet.Name <> "Input_Sheet_Template" Then Exit Sub
    '****************************error handling***************************

    '=HLOOKUP(startup_year,Tbl_Other_Inputs_and_Byproducts,MATCH(TMP_NonE_Feed,Other_Inputs_List,0),FALSE)
    
If ActiveSheet.Shapes("Rounded Rectangle 50").Fill.ForeColor.RGB = RGB(128, 128, 225) Then
       ActiveSheet.Shapes("Rounded Rectangle 50").Fill.ForeColor.RGB = RGB(255, 204, 153)
       ActiveSheet.Shapes("Rounded Rectangle 50").TextFrame.Characters.Text = "Enter Cost Manually"
        ActiveSheet.Shapes("Rounded Rectangle 50").TextFrame.Characters.Font.Color = RGB(0, 0, 0)

    
        'lblUseOtherDefault.Visible = False
        Application.Range("TMP_nonE_Escalation").Value = "No"
        Application.Goto reference:="TMP_nonE_StartPrice"
        Call InputCell
        Application.Range("TMP_nonE_StartPrice").Value = ""

ElseIf ActiveSheet.Shapes("Rounded Rectangle 50").Fill.ForeColor.RGB = RGB(255, 204, 153) Then
   ActiveSheet.Shapes("Rounded Rectangle 50").Fill.ForeColor.RGB = RGB(128, 128, 225)
   ActiveSheet.Shapes("Rounded Rectangle 50").TextFrame.Characters.Text = "Use Cost Tables"
   ActiveSheet.Shapes("Rounded Rectangle 50").TextFrame.Characters.Font.Color = RGB(255, 255, 255)

    
        'lblUseOtherDefault.Visible = True
        Application.Range("TMP_nonE_Escalation").Value = "Yes"
        Application.Goto reference:="TMP_nonE_StartPrice"
        Call CalculatedCell
        Application.Range("TMP_nonE_StartPrice").Value = "=HLOOKUP(startup_year,Tbl_Other_Inputs_and_Byproducts,MATCH(TMP_NonE_Feed,Other_Inputs_List,0),FALSE)"
    End If
    Exit Sub
ErrHandler:
    MsgBox "Error in TglUseOtherPrice sub"

End Sub

Sub AddTwo()

 Dim FeedType As String
    Dim InsertLocName As String
    Dim InsertLocRow As Long
    Dim InsertRowsTxt As String 'lazy lazy lazy
    Dim FeedUse As Double 'the amount used/kg H2 = TMP_NonE_Usage
    
    '****************************error handling***************************
    'On Error GoTo ErrHandler
    If Working = True Then Exit Sub
    'if the input sheet is not the active sheet, exit the sub
    If ActiveSheet.Name <> "Input_Sheet_Template" Then Exit Sub
    'get the values for the variables
    FeedUse = Application.Evaluate("TMP_NonE_Usage").Value
    If FeedUse = 0 Then
        MsgBox "Please enter a value for the non energy feed usage"
        Exit Sub
    End If
    '****************************error handling***************************
    
    FeedType = CStr(Application.Evaluate("tmp_NonE_Type").Value)
    Select Case FeedType
        Case "Feed or utility"
            InsertLocName = "START_NONE_FEED"
        Case "Byproduct"
            InsertLocName = "START_NONE_BYPROD"
        Case Else
            InsertLocName = "STOP"
    End Select
    If InsertLocName = "STOP" Then Exit Sub
    'link the values to the appropriate named ranges
    'Call SetNonEVariables
    Application.Goto reference:=InsertLocName
    InsertLocRow = Selection.Row
    InsertRowsTxt = CStr(InsertLocRow) & ":" & CStr(InsertLocRow + 1)
    Rows(InsertRowsTxt).Select
    Selection.Insert Shift:=xlDown

    
    Range("VAR_NonE_FEED_VALUES").Select
    Selection.Copy
    Cells(InsertLocRow, 2).Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=True
    
     'first define the locations for the cells that will be referenced
    Dim FeedNameCell As Range
    Dim UsageCell As Range
    Dim LookupCell As Range
    Dim PriceCell As Range
    
    Set FeedNameCell = Cells(InsertLocRow + 1, 2)
    Set UsageCell = Cells(InsertLocRow + 1, 4)
    Set LookupCell = Cells(InsertLocRow + 1, 6)
    Set PriceCell = Cells(InsertLocRow + 1, 3)
    
    Call OtherYearlyCost(FeedType, FeedNameCell, UsageCell, LookupCell, PriceCell)
    
    
    'Clean up
    Application.Goto reference:="TMP_NonE_Usage"
    Selection.ClearContents
    Application.Goto reference:="TMP_NonE_Escalation"
    Selection.Value = "Yes"
    
    'chkNonEnergyByProd.Value = False
    'tglEnterOtherPrice.Value = False
    Exit Sub
ErrHandler:
    MsgBox "Error in cmdAddNonE event"

End Sub

Sub DeleteTwo()
    Toolkit_Control_Panel.Show vbModal

End Sub
Sub EnterSpecificCosts()
    'go to the detail cost sheet (Replacement Costs)
    Worksheets("Replacement Costs").Activate
    ActiveSheet.Range("$A$1").Select

End Sub
