from dataclasses import dataclass
import xml.etree.ElementTree as ET
from typing import List

def read_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip().replace(":443", "")

    return lines

def find_duplicate_files(lines):
    files = set()
    duplicates = []
    for line in lines:
        if line.split("/")[-1] in files:
            duplicates.append(line.split("/")[-1])
        else:
            files.add(line.split("/")[-1])
    return duplicates

def find_topics(lines):
    topics = {}
    for line in lines:
        topic_url = "/".join(line.split("/")[:-1])
        topic, file_name = line.split("/")[-2:]

        title = clean_title(topic)
        if title == "Vritasur Katha":
            file_name = f"Vritasur Katha {file_name[-6:-4]}"
        file = File(url=line, title=create_file_title(file_name))

        if title not in topics:
            topics[title] = Topic(url=topic_url, files=[file], title=title)
        else:
            topics[title].files.append(file)

    for topic in topics:
        topics[topic].files.sort(key=lambda x: x.title)
        print(topic)
        for file in topics[topic].files:
            print("\t", file.title)
    
    return topics

def clean_title(title):
    title = title.lower()
    title = title.replace('rgs', '')

    if "canto" not in title:
        title = title.lstrip('0123456789_')
        title = title.rstrip('0123456789_')

    title = title.replace('_', ' ').title()


    if "- " == title[:2]:
        title = title[2:]
    
    title = title.split("-Sb")[0]
    title = title.split(" Sb ")[0]
    title = title.split("-Cc")[0]
    title = title.split(" - ")[0]
    return title.strip().title()

def create_file_title(file_name):
    title = file_name.lower()
    title = title.replace('rgs', '')
    title = title.split('.')[0]
    return title.replace('_', ' ').title().strip()

@dataclass
class File:
    title: str
    url: str

@dataclass
class Topic:
    title: str
    url: str
    files: list[File]

def channelize(topic):
    items = []
    for file in topic.files:
        item = Item(
            title=file.title,
            author="Radha Govinda Das Goswami Maharaj",
            pubDate="",
            enclosure_length="0",
            enclosure_type="audio/mpeg",
            enclosure_url=file.url,
            description=""
            )
        items.append(item)
    
    channel = Channel(
        title=topic.title,
        author="Radha Govinda Das Goswami Maharaj",
        image_url="https://i1.sndcdn.com/artworks-000115964927-iks7g4-t500x500.jpg",
        image_title="Radha Govinda Das Goswami Maharaj",
        image_link=r"https://audio.iskcondesiretree.com/index.php?q=f&f=%2F02_-_ISKCON_Swamis%2FISKCON_Swamis_-_R_to_Y%2FHis_Holiness_Radha_Govinda_Swami",
        description="",
        language="en",
        pub_date="",
        link=r"https://audio.iskcondesiretree.com/index.php?q=f&f=%2F02_-_ISKCON_Swamis%2FISKCON_Swamis_-_R_to_Y%2FHis_Holiness_Radha_Govinda_Swami",
        items=items
    )
    return channel

@dataclass
class Item:
    title: str
    author: str
    pubDate: str
    enclosure_url: str
    enclosure_type: str
    enclosure_length: str
    description: str

@dataclass
class Channel:
    title: str
    author: str
    image_url: str
    image_title: str
    image_link: str
    description: str
    language: str
    pub_date: str
    link: str
    items: List[Item]


    def to_rss(self, filename: str):
        channel_elem = ET.Element('channel')

        title_elem = ET.SubElement(channel_elem, 'title')
        title_elem.text = self.title

        author_elem = ET.SubElement(channel_elem, 'author')
        author_elem.text = self.author

        image_elem = ET.SubElement(channel_elem, 'image')
        image_url_elem = ET.SubElement(image_elem, 'url')
        image_url_elem.text = self.image_url
        image_title_elem = ET.SubElement(image_elem, 'title')
        image_title_elem.text = self.image_title
        image_link_elem = ET.SubElement(image_elem, 'link')
        image_link_elem.text = self.image_link


        # ... add remaining channel elements ...

        for item in self.items:
            item_elem = ET.SubElement(channel_elem, 'item')
            
            author = ET.SubElement(item_elem, 'author')
            author.text = item.author

            title = ET.SubElement(item_elem, 'title')
            title.text = item.title

            enclosure = ET.SubElement(item_elem, 'enclosure')
            enclosure.set('url', item.enclosure_url)
            enclosure.set('type', item.enclosure_type)

        rss_elem = ET.Element('rss')
        rss_elem.set('xmlns:googleplay', 'http://www.google.com/schemas/play-podcasts/1.0')
        rss_elem.set('xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
        rss_elem.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss_elem.set('xmlns:rawvoice', 'http://www.rawvoice.com/rawvoiceRssModule/')
        rss_elem.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss_elem.set('version', '2.0')

        rss_elem.append(channel_elem)

        ET.ElementTree(rss_elem).write(filename, encoding='UTF-8', xml_declaration=True)

if __name__ == "__main__":
    lines = read_file("./examples/RGS-playlist.m3u")
    topics = find_topics(lines)
    for topic in topics:
        channel = channelize(topics[topic])
        channel.to_rss(f"./rss-feed/{topic}.xml")
        break