import os

dir_path = "./rss-feed/RGS/"

with open("./rss-feed/RGS.opml", "w") as f:
    f.write('<?xml version="1.0"?>\n')
    f.write('<opml version="1.0">\n')
    f.write('  <head>\n')
    f.write('    <title>My RSS Feeds</title>\n')
    f.write('  </head>\n')
    f.write('  <body>\n')
    
    for filename in os.listdir(dir_path):
        if filename.endswith(".xml"):
            f.write(f'    <outline type="rss" text="{filename}" title="{filename}" xmlUrl="{os.path.join("https://github.com/kendreaditya/RSS-podcasts/raw/main/rss-feed/RGS/", filename)}" />\n')
    
    f.write('  </body>\n')
    f.write('</opml>')
