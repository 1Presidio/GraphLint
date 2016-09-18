#!/usr/bin/python2.7

# TODO Investigate defusedxml
import xml.etree.ElementTree as et
import os, os.path, shutil
import zipfile as zf

app_root = "/Users/Kevin/Desktop/HackCMU2016/"

def make_suggestions(filename):
    retval = {"suggestions" : []}
    uploaded_file = filename
    tmp_dir = app_root+"/tmp_dir"

    uploaded_file_cp = os.path.join(tmp_dir, os.path.basename(uploaded_file))

    os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    shutil.copyfile(uploaded_file, uploaded_file_cp)
    zf.ZipFile(uploaded_file_cp).extractall()

    chart_file = "Object 1/content.xml"
    doc_file = "content.xml"

    odf_chart = "{urn:oasis:names:tc:opendocument:xmlns:chart:1.0}"
    odf_table = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"

    #
    # Read in the XML data
    #
    chart_tree = et.parse(chart_file)
    chart_root = chart_tree.getroot()
    doc_tree = et.parse(doc_file)
    doc_root = doc_tree.getroot()

    #
    # Perform the checks for graphs
    #

    # Use captions and labels

    ## Caption present

    ## Axis-labels present
    for axis in chart_root.iter(odf_chart+"axis"):
        if "z" in axis.attrib[odf_chart+"name"]:
            continue
        if axis.find(odf_chart+"title") is None:
            retval["suggestions"].append("add a title to the "+axis.attrib[odf_chart+"name"][-1]+" axis")
        # else:
        #     print axis.attrib[odf_chart+"name"][-1], "axis has a title"
    ## Legend present
    first = next(chart_root.iter(odf_chart+"legend"), None)
    if first is None:
        retval["suggestions"].append("add a legend")
    # else:
    #     print "legend found"

    # Sort [numerical] data
    # for table in chart_root.iter(odf_table+"table"):
    #     for row in table.iter(odf_table+"table-row"):

    # Reduce non-data ink
    ## Remove axis grid lines
    for axis in chart_root.iter(odf_chart+"axis"):
        if "z" in axis.attrib[odf_chart+"name"]:
            continue
        if axis.find(odf_chart+"grid") is not None:
            retval["suggestions"].append("remove grid lines for the "+axis.attrib[odf_chart+"name"][-1]+" axis")
        # else:
        #     print axis.attrib[odf_chart+"name"][-1], "axis does not have grid lines"
        ## Call out 3D effects
    for axis in chart_root.iter(odf_chart+"axis"):
        if "z" in axis.attrib[odf_chart+"name"]:
            retval["suggestions"].append("don't use 3D effects")

    # Minimize eye movement

    # Emphasize contrast

    # Use consistent numbering

    #
    # Perform the checks for tables
    #

    #
    #
    # Jeremy
    #
    #

    ##check table
    table_file = "Object 2/content.xml"

    table_tree = et.parse(table_file)
    table_root = table_tree.getroot()

    odf_style = "{urn:oasis:names:tc:opendocument:xmlns:style:1.0}"
    odf_office = "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}"
    # odf_table = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}" 
    odf_fo = "{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}"

    ## Column and row widths up to standard
    finalArray = list()

    rowError = "Adjust the height of your rows to 20pt"
    rowPass = "Your row heights are super!"
    rowResult = ""
    listOfRows = list()
    counter = 1
    for rows in table_root.iter(odf_style+"style"):
        if rows.attrib[odf_style+"name"].startswith("ro"):
            listOfRows.append(rows.attrib[odf_style+"name"])
    for rowProperty in table_root.iter(odf_style+"table-row-properties"):
        heightOfRow = rowProperty.attrib[odf_style+"row-height"]
        while (counter < len(listOfRows)):
            if heightOfRow != "20.01pt":
                rowProperty.attrib[odf_style+"row-height"] = "20.01pt"
                rowResult = rowError
            else:
                if rowResult == rowError: continue
                else: rowResult = rowPass
            counter += 1
    # finalArray.append(rowResult)

    columnError = "Adjust the width of your columns to fit your text"
    columnPass = "Your column widths are great!"
    columnResult = ""
    numOfColumns = 0
    counter = 1
    for cols in table_root.iter(odf_style+"style"):
        if cols.attrib[odf_style+"name"].startswith("co"):
            numOfColumns += 1
    for colProperty in table_root.iter(odf_style+"table-column-properties"):
        widthOfColumn = colProperty.attrib[odf_style+"column-width"]
        if widthOfColumn == "92.1pt":
            columnResult = columnError
        else:
            if columnResult == columnError: continue
            else: columnResult = columnPass
        counter += 1
    finalArray.append(columnResult)
    # print finalArray

    ## Borders
    #Head Border test
    headBorderResult = ""
    headBorderError = "Only use top and bottom borders for your table heading labels"
    headBorderPass = "Your header labels are fine!" 
    for style in table_root.iter(odf_style+"table-cell-properties"):
        if odf_fo+"border" in style.attrib.keys():
            headBorderResult = headBorderError
        else:
            headBorderResult = headBorderPass
        if odf_fo+"border-left" in style.attrib.keys() and style.attrib[odf_fo+"border-left"] == "none":
            headBorderResult = headBorderPass
        else:
            headBorderResult = headBorderError
        break
    finalArray.append(headBorderResult)
    # print finalArray

    #Bottom Border test
    bottomBorderResult = ""
    bottomBorderError = "Only use bottom borders for your last line and no lines for the body of the table"
    bottomBorderPass = "Your bottom labels are perfect!" 
    for style in table_root.iter(odf_style+"table-cell-properties"):
        if odf_fo+"border" in style.attrib.keys():
            bottomBorderResult = bottomBorderError
        else:
            bottomBorderResult = bottomBorderPass
    if (bottomBorderResult == bottomBorderPass):
        for style in table_root.iter(odf_style+"table-cell-properties"):
            if (odf_fo+"border-left" in style.attrib.keys() and 
                style.attrib[odf_fo+"border-left"] == "none" and 
                odf_fo+"border-top" in style.attrib.keys() and
                style.attrib[odf_fo+"border-top"] == "none" and
                odf_fo+"border-right" in style.attrib.keys() and
                style.attrib[odf_fo+"border-right"] == "none"):
                    bottomBorderResult = bottomBorderPass
            else:
                bottomBorderResult = bottomBorderError
    finalArray.append(bottomBorderResult)
    # print finalArray

    retval["suggestions"] += finalArray

    #
    #
    # Jeremy
    #
    #

    os.chdir("../")
    shutil.rmtree(tmp_dir)

    return retval

#
# Flask magic
#
from flask import Flask, request
from flask.ext import restful
from flask.ext import uploads
app = Flask(__name__)
api = restful.Api(app)

import urllib2

# docs = uploads.UploadSet('docs', 'odt')

# localhost:3000/results

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # print request.method
    # print request.files
    if request.method == 'POST' and 'doc.odt' in request.files:
        uploaded_file = request.files['doc.odt']
        if uploaded_file.filename != "":
            saved_filename = os.path.join(tmp_dir, "doc.odt")
            uploaded_file.save(saved_filename)

            post_url = "http://localhost:3000/results"
            data = suggest_changes(saved_filename)
            content = urllib2.urlopen(url=url, data=data)

# api.add_resource(SuggestChanges, '/')

# print make_suggestions(app_root+"09_16_final.odt")

# if __name__ == "__main__":
#     app.run(debug=True)
