Option Explicit
Public Sub UseDefaults(ByVal VarList As String)
    'This sub is called from a button in the TOC for each input sheet
    'For "use defaults for blank values", check the default checkboxes on the selected sheet.
    'If the input cell is blank, use the default and check the box
    'If the input cell is not blank, check or uncheck the box depending on what is in the input cell.
    'For "Use defaults for all values", fill all the input cells with defaults and check the boxes.

    Dim VarCell As Range
    Dim DfltList As Range
    Dim VarDflt As String 'default value
    Dim DfltName As String
    Dim chkName As String
    Dim ShtName As String
    
    If Working = True Then Exit Sub
    On Error GoTo ErrorCode:
    
    Select Case VarList
        Case "Input_Value_Defaults"
            Set DfltList = Application.Range("Input_Value_Defaults")
            ShtName = "Input_Sheet_Template"
        Case "CO2_Value_Defaults"
            Set DfltList = Application.Range("CO2_Value_Defaults")
            ShtName = "Carbon Sequestration"
        Case "Refueling_Value_Defaults" 'this is not being used in the central model
            Set DfltList = Application.Range("Refueling_Value_Defaults")
            ShtName = "Refueling Station"
        Case Else
    End Select
    
    Set DfltList = DfltList.Resize(DfltList.Rows.Count, DfltList.Columns.Count - 1)
    
    'Find out whether the user wants to replace blank values or all values - replace all values
    'will be the default
    Dim ans As VbMsgBoxResult
    ans = MsgBox("Replace all values on this page with default values?" & vbCrLf & "Click Yes to replace all values. Click No to only replace blanks with default values", 259)
    If ans = vbCancel Then
        Exit Sub
    Else
        If ans = vbYes Then 'Replace all values
            For Each VarCell In DfltList.Cells
                DfltName = VarCell.Cells(1, 1).Value
                chkName = "chk_" & DfltName
                VarDflt = VarCell.Offset(0, 1).Cells(1, 1).Value
                With Worksheets(ShtName)
                    Application.Range(DfltName).Value = VarDflt
                    .OLEObjects(chkName).Object.Value = True
                End With
            Next VarCell
        Else 'Replace blanks only
            For Each VarCell In DfltList.Cells
                DfltName = VarCell.Cells(1, 1).Value
                chkName = "chk_" & DfltName
                VarDflt = VarCell.Offset(0, 1).Cells(1, 1).Value
                With Worksheets(ShtName)
                    If Application.Range(DfltName).Value = "" Then
                        Application.Range(DfltName).Value = VarDflt
                        .OLEObjects(chkName).Object.Value = True
                    Else
                        If Application.Range(DfltName).Value = VarDflt Then
                            .OLEObjects(chkName).Object.Value = True
                        Else
                            .OLEObjects(chkName).Object.Value = False
                        End If
                    End If
                End With
            Next VarCell
        End If
    End If
    Exit Sub
ErrorCode:
    Exit Sub
End Sub
Public Sub AssignEmissionsTable(ByVal StartYear As Integer)
    'Assign the correct emissions table to the Name "Tbl_Emissions" based on the startup year
'    Dim SelectedTable As String
'    Select Case StartYear
'        Case Is < 2020
'            SelectedTable = "Tbl_2005Emissions"
'        Case Else
'            SelectedTable = "Tbl_2020Emissions"
'    End Select
'    ActiveWorkbook.Names.Add Name:="Tbl_Emissions", RefersTo:=ActiveWorkbook.Names(SelectedTable)
            
            ' disabled this feature to allow time series sensitivity
                Dim SelectedTable As String
'                Select Case StartYear
'                    Case Is < 2020
                        SelectedTable = "Tbl_2005Emissions"
'                    Case Else
'                        SelectedTable = "Tbl_2020Emissions"
'                End Select
                ActiveWorkbook.Names.Add Name:="Tbl_Emissions", RefersTo:=ActiveWorkbook.Names(SelectedTable)
End Sub
Public Sub AssignNames()
    'the user has put the names in the cells to the right of the cells to name and selected the cells
    Dim AssignRange As Range
    
    On Error Resume Next
    Set AssignRange = Application.InputBox(prompt:="Put the names in cells to the right of the cells to name.  Select both the cells to name and the cells with the names and click ok", Type:=8)
    AssignRange.CreateNames Right:=True
    
End Sub
Public Sub AddtoSensList(ByVal TxtName As String, ByVal VarName As String)
    'Add the feedstock variables to the sensitivity analysis list
    'Insert cells at the top of the list
    Dim InsertRow As Long
    Dim InsertClm As Long
    
    Worksheets("Lists").Activate
    Application.Goto reference:="Sensitivity_Variables"
    Selection.Activate
    InsertRow = Selection.End(xlDown).Row + 1
    Selection.Cells(1, 1).Select
    InsertClm = Selection.Column
    With Worksheets("Lists")
        .Range(.Cells(InsertRow, InsertClm), .Cells(InsertRow, InsertClm + 1)).Select
        'Selection.Insert Shift:=xlDown
        .Cells(InsertRow, InsertClm).Value = TxtName
        .Cells(InsertRow, InsertClm + 1).Value = VarName
    End With
    
End Sub
Public Function AssignSensitivityNames(ByVal FeedType As String, ByVal NameCell As Range, ByVal RefCell As Range, ByVal EndTxt As String) As String
    'Assign names to the price and usage cells so that they can be varied in the sensitivity analysis
    'Function returns the name assigned to the cell
    
    Dim SensVarName As String
    Dim NewName As String
    
    NewName = Replace(CStr(NameCell.Value), " ", "_")
    
    SensVarName = FeedType & NewName & EndTxt
    Application.Names.Add Name:=SensVarName, RefersTo:=RefCell
    
    AssignSensitivityNames = SensVarName
    
End Function
Public Function CalcH2Price(ByVal VarName As String, ByVal VarValue As Double) As Double
'save the reference location for the variable, re-assign the variable to the VarValue, recalculate
'the H2 price, return it, assign the variable back to the original location.

    'first, locate the variable and give it a name to locate it later
    Application.Goto reference:=Range(VarName)
    ActiveWorkbook.Names.Add Name:="HoldLocation", RefersTo:=Range(VarName)
    're-assign the variable to the value passed to the function
    Application.Goto reference:="Temp_Var_Location"
    Selection.Value = VarValue
    ActiveWorkbook.Names.Add Name:=VarName, RefersTo:=Range("Temp_Var_Location")
    
    'Calculate a new H2 price
    Call Solve_NPV
    CalcH2Price = Application.Evaluate("Result_Price").Value
    
    're-assign the variable to its original location and "Temp_Var_Location" back to its location on "Lists"
    ActiveWorkbook.Names.Add Name:="Temp_Var_Location", RefersTo:=Range(VarName)
    ActiveWorkbook.Names.Add Name:=VarName, RefersTo:=Range("HoldLocation")
    ActiveWorkbook.Names("HoldLocation").Delete
    
End Function

Public Function FeedstockYearlyCost(ByVal eFeedType As String, ByVal FeedNameCell As Range, ByVal LHVCell As Range, ByVal UsageCell As Range, ByVal LookupCell As Range, ByVal PriceCell As Range, ByVal UsageVarName As String, ByVal PriceVarName As String) As Boolean
    'when the user selects a feedstock from the dropdown list, has entered values and clicked "Add",
    'fill in the table of prices by year for the feed.
    'try referring to the first year price info just added to new rows on the input sheet
    'ok, but need to refer to variable names for usage and price so the values can be used in sensitivity analysis
    
    'First locate the next available spot in the table of yearly prices
    Dim NextColumn As Long
    Dim NameRow As Long 'locate the column and row on the "cash flow analysis" spreadsheet in which to
                        'put the references back to the input sheet.
    Dim NextCell As Range
    Dim CaseList As Range
    
    FeedstockYearlyCost = False 'no available space
    
    Select Case eFeedType
        Case "feedstock"
            Set CaseList = Application.Range("Case_eFeed_List")
        Case "utility"
            Set CaseList = Application.Range("Case_eUtility_List")
        Case "byproduct"
            Set CaseList = Application.Range("Case_eByprod_List")
        Case Else
    End Select
    For Each NextCell In CaseList
        If NextCell.Text = "" Then
            NextColumn = NextCell.Column
            NameRow = NextCell.Row
            FeedstockYearlyCost = True 'a space was found
            Exit For
        End If
    Next NextCell
    If FeedstockYearlyCost = False Then Exit Function 'there is no space
    
    Worksheets("cash flow analysis").Cells(NameRow, NextColumn).Formula = "=Input_Sheet_Template!" & FeedNameCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 1, NextColumn).Formula = "=Input_Sheet_Template!" & LHVCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 2, NextColumn).Formula = "=" & UsageVarName 'Input_Sheet_Template!" & UsageCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 3, NextColumn).Formula = "=" & PriceVarName 'Input_Sheet_Template!" & PriceCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 4, NextColumn).Formula = "=Input_Sheet_Template!" & LookupCell.Address
    
End Function
Public Sub OtherYearlyCost(ByVal MaterialType As String, ByVal FeedNameCell As Range, ByVal UsageCell As Range, ByVal LookupCell As Range, ByVal PriceCell As Range)
    'when the user selects a material from the dropdown list, has entered values and clicked "Add",
    'fill in the table of prices by year for the feed.
    'try referring to the first year price info just added to new rows on the input sheet
    
    'First locate the next available spot in the table of yearly prices
    Dim NextColumn As Long
    Dim NameRow As Long 'locate the column and row on the "cash flow analysis" spreadsheet in which to
                        'put the references back to the input sheet.
    Dim NextCell As Range
    Dim CaseList As Range
    Select Case MaterialType
        Case "Feed or utility"
            Set CaseList = Application.Range("Case_material_input_List")
        Case "Byproduct"
            Set CaseList = Application.Range("Case_material_byprod_List")
        Case Else
    End Select
    For Each NextCell In CaseList
        If NextCell.Text = "" Then
            NextColumn = NextCell.Column
            NameRow = NextCell.Row
            Exit For
        End If
    Next NextCell
    Worksheets("cash flow analysis").Cells(NameRow, NextColumn).Formula = "=Input_Sheet_Template!" & FeedNameCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 1, NextColumn).Formula = "=Input_Sheet_Template!" & UsageCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 2, NextColumn).Formula = "=Input_Sheet_Template!" & PriceCell.Address
    Worksheets("cash flow analysis").Cells(NameRow + 3, NextColumn).Formula = "=Input_Sheet_Template!" & LookupCell.Address
'=Input_Sheet_Template!$B$100
    
End Sub
