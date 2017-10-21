# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project_dbsetup import User, Author, Work_titles, Discussion, Base

engine = create_engine('sqlite:///authorsandworktitles.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


author1 = Author(name="Aldous Huxley", country="United Kingdom",
                     dob="26/7/1884", category="dark")

session.add(author1)
session.commit()

author2 = Author(name="Franz Kafka", country="Czech Republic",
                     dob="3/7/1883", category="dark")

session.add(author2)
session.commit()

author3 = Author(name="Friedric Nietzsche", country="Germany",
                     dob="15/10/1884", category="dark")

session.add(author3)
session.commit()

author4 = Author(name="George Orwell", country="United Kingdom",
                     dob="25/6/1903", category="dark")

session.add(author4)
session.commit()

author5 = Author(name="Henry David Thoreau", country="USA",
                     dob="12/7/1817", category="light")

session.add(author5)
session.commit()

author6 = Author(name="Karl Marx", country="Germany",
                     dob="5/5/1809", category="light")

session.add(author6)
session.commit()

author7 = Author(name="Nicholas Nassim Taleb", country="USA",
                     dob="1/1/1960", category="dark")

session.add(author7)
session.commit()

author8 = Author(name="Rabindranath Tagore", country="India",
                     dob="7/5/1861", category="light")

session.add(author8)
session.commit()

author9 = Author(name="Soren Kierkeggard", country="Denmark",
                     dob="5/5/1813", category="light")

session.add(author9)
session.commit()

author10 = Author(name="Victor Frankl", country="Austria",
                     dob="26/3/1905", category="light")

session.add(author10)
session.commit()


work_title1 = Work_titles(author_id="1", work_title="Brave New World", category="Book",
             summary=u"The natural processes of birth, aging, and death represent horrors in this world. Bernard Marx, an Alpha-Plus or high-caste psychologist, emerges as the single discontented person in a world where material comfort and physical pleasure are the only concerns.", author=author1)

session.add(work_title1)
session.commit()

work_title2 = Work_titles(author_id="2", work_title="Metamorphosis", category="Book",
             summary=u"Gregor is the main character of the story. He works as a traveling salesman in order to provide money for his sister and parents. He wakes up one morning finding himself transformed into an insect. After the metamorphosis, Gregor becomes unable to work and is confined to his room for the remainder of the story.",
             author=author2)

session.add(work_title2)
session.commit()

work_title3 = Work_titles(author_id="3", work_title="Beyond Good and Evil", category="Book",
             summary=u"A world of rigid facts can be spoken about definitively, which is the source of our conception of truth and other absolutes, such as God and morality. Nietzsche sees the facts and things of traditional philosophy as far from rigid, and subject to all sorts of shifts and changes.",
             author=author3)

session.add(work_title3)
session.commit()

work_title4 = Work_titles(author_id="4", work_title="1984", category="Book",
             summary=u"In George Orwell's 1984, Winston Smith wrestles with oppression in Oceania, a place where the Party scrutinizes human actions with ever-watchful Big Brother. Defying a ban on individuality, Winston dares to express his thoughts in a diary and pursues a relationship with Julia.",
             author=author4)

session.add(work_title4)
session.commit()

work_title5 = Work_titles(author_id="5", work_title="Walden", category="Book",
             summary=u"Walden serves as a written account of the two years Henry David Thoreau lived alone in a cabin in Concord, Massachusetts. He built this cabin, grew vegetables, and had transcendental experiences. He uses these to examine the fundamental elements of identity. Thoreau builds himself a small cabin on Walden Pond.",
             author=author5)

session.add(work_title5)
session.commit()

work_title6 = Work_titles(author_id="6", work_title="Das Kapital", category="Book",
             summary=u"Das Kapital, one of the major works of the 19th-century economist and philosopher Karl Marx (1818–83), in which he expounded his theory of the capitalist system, its dynamism, and its tendencies toward self-destruction.",
             author=author6)

session.add(work_title6)
session.commit()

work_title7 = Work_titles(author_id="7", work_title="Anti Fragile", category="Book",
             summary=u"The author, Nassim Nicholas Taleb, is a statistician and investigates problems of randomness and uncertainty. He argues that some systems thrive when exposed to shocks and crises, instead of breaking under their pressure.",
             author=author7)

session.add(work_title7)
session.commit()

work_title8 = Work_titles(author_id="8", work_title="Gitanjali", category="Poetry",
             summary=u"Gitanjali Song Offerings is a collection of 103 prose poems, selected by Tagore from among his Bengali poems and translated by him into English. The collection brought Tagore international attention and won him the Nobel Prize in Literature.",
             author=author8)

session.add(work_title8)
session.commit()

work_title9 = Work_titles(author_id="9", work_title="Tractatus", category="Book",
             summary=u"Philosophy, unlike science, is not a body of propositions. It should be thought of as the activity of clarifying the often obscure logical structure of language and thought.",
             author=author9)

session.add(work_title9)
session.commit()

work_title10 = Work_titles(author_id="10", work_title="Man's Search for Meaning", category="Book",
             summary=u"Man's Search for Meaning Summary. Man's Search For Meaning is a work of non-fiction that deals with Viktor Frankl's experience living in Nazi concentration camps, as well as his psychotherapeutic technique called logotherapy.",
             author=author10)

session.add(work_title10)
session.commit()

discussion1 = Discussion(message="Random text message 1 ahfohdofhsofhodshfosdhfiohdsoifjapjsapddjspfjpajpfjaspfjaspj", date_created="1/1/2016", user_id="1", work_id="1")

session.add(discussion1)
session.commit()

discussion2 = Discussion(message="Random text message 2 xjzbkbzkfqbofwhqohwfowqhfohqwsaasdasdasdadasd", date_created="1/2/2016", user_id="1", work_id="1")

session.add(discussion2)
session.commit()

discussion3 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="2")

session.add(discussion3)
session.commit()

discussion4 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="2")

session.add(discussion4)
session.commit()

discussion5 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="3")

session.add(discussion5)
session.commit()

discussion6 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="3")

session.add(discussion6)
session.commit()

discussion7 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="4")

session.add(discussion7)
session.commit()

discussion8 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="4")

session.add(discussion8)
session.commit()

discussion9 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="5")

session.add(discussion9)
session.commit()

discussion10 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="5")

session.add(discussion10)
session.commit()

discussion11 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="6")

session.add(discussion11)
session.commit()

discussion12 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="6")

session.add(discussion12)
session.commit()

discussion13 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="7")

session.add(discussion13)
session.commit()

discussion14 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="7")

session.add(discussion14)
session.commit()

discussion15 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="8")

session.add(discussion15)
session.commit()

discussion16 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="8")

session.add(discussion16)
session.commit()

discussion17 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="9")

session.add(discussion17)
session.commit()

discussion18 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="9")

session.add(discussion18)
session.commit()

discussion19 = Discussion(message="Random text message 1 bkzbcoqwhphoihdoqwhoqwhoewhqoewhoewqhoh", date_created="1/3/2016", user_id="2", work_id="10")

session.add(discussion19)
session.commit()

discussion20 = Discussion(message="Random text message 2 hqowhowqhoinonconconwqoidinwiqodnowqndoqwnon", date_created="1/4/2016", user_id="2", work_id="10")

session.add(discussion20)
session.commit()
