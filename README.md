django\_mailman\_search
=====================

A Django project to search the Mailman email archives.


Installation
==========

Install the Python/Django dependencies as

```
pip install pip_requirements.txt
```

followed by

```
python manage.py syncdb
```

to create the database.


URLs
=======

- The landing page can be accessed at ```/emails/``` where you can search by your keyword(s).
- The query search is sent to ```/search/``` where the search results are displayed
- Details of a particular search result (i.e., a specific email) can be viewed at ```/emails/id/```

The HTML templates have been kept minimum so that the essential code for searching and display can be easily understood.


Indexing the archives
==================

Two management commands are provided -- ```load_archive``` and ```clear_archive```. The former parses the email archives and loads the corresponding entries into the database. The latter one removes all existing records from the database. The Django app ```emails``` handles these.

To load email archives into the database:

```
python manage.py load_archive
```

This should be done before the first use and every time you have some new archive. Note that the archive files are not automagically downloaded -- you should ensure that those files are stored at the ```archive/files/``` directory. If you change this location, update the ```load_archive.py``` script accordingly.

Currently, a few emails (and references) could not be loaded into the database due to some malformed attributes including, but not limited to, email address. However, this would be a very low percentage.

To build the index:

```
python manage.py rebuild_index
```

To update the index:

```
python manage.py update_index
```


For advanced users
====================

The ```models.py``` file defines two models -- ```Email``` and ```References```. The former abstracts an email together with its contents. However, in a mailing list, one can reply to an email, which can be further replied to. Such emails refer to the previous emails by their message IDs.

Additionally, such emails also have a ```Reply to``` field, which, however, is not handled currently.

TODO
======

- Display an entire email chain
- Add test cases
