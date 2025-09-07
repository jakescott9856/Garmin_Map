import parse_fit
import graph
from datetime import date
fdate = date.today().strftime('%d/%m/%Y')

User = 'JS'
Map_display = 'All'
#Red_modified = fdate  
Red_modified= '01/01/2099'

parse_fit.main(User)
graph.main(User,Map_display,Red_modified)