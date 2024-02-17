# index.py file
import base64
import datetime as dt
import io
import random
import jinja2
import matplotlib.pyplot as plt

# Step 1 - create data for report
salesTblRows = []
for k in range(10):
    costPu = random.randint(1, 15)
    nUnits = random.randint(100, 500)
    salesTblRows.append({"sNo": k+1, "name": "Item "+str(k+1),
                         "cPu": costPu, "nUnits": nUnits, "revenue": costPu*nUnits})

topItems = [x["name"] for x in sorted(
    salesTblRows, key=lambda x: x["revenue"], reverse=True)][0:3]

todayStr = dt.datetime.now().strftime("%d-%b-%Y")


# generate sales bar chart image
plotImgBytes = io.BytesIO()
fig, ax = plt.subplots()
ax.bar([x["name"] for x in salesTblRows], [x["revenue"] for x in salesTblRows])
fig.tight_layout()
fig.savefig(plotImgBytes, format="jpg")
plotImgBytes.seek(0)
plotImgStr = base64.b64encode(plotImgBytes.read()).decode()

# data for injecting into jinja2 template
context = {
    "reportDtStr": todayStr,
    "salesTblRows": salesTblRows,
    "topItemsRows": topItems,
    "salesBarChartImg": plotImgStr,

}

# Step 2 - create jinja template object from file
template = jinja2.Environment(
    loader=jinja2.FileSystemLoader("./templates"),
    autoescape=jinja2.select_autoescape
).get_template(".reports/sales.html")

# Step 3 - render data in jinja template
reportText = template.render(context)

# Step 4 - Save genereate text as a HTML file
reportPath = "./reports/sale.html"
with open(reportPath, mode='w') as f:
    f.write(reportText)
