"""
From Chris McDonough:

If it's not labeled otherwise and it comes from us, it's released under this license... http://repoze.org/license.html (BSD-like)...

"""

import os
import setuptools
import shutil
import subprocess
import sys
import tarfile
import zipfile
import tempfile

class TarArchive:
    def __init__(self, filename):
        self.filename = filename
        self.tgz = tarfile.TarFile.gzopen(filename, 'r')

    def names(self):
        return self.tgz.getnames()

    def lines(self, name):
        return self.tgz.extractfile(name).readlines()

    def extract(self, name, tempdir):
        return self.tgz.extract(name, tempdir)

    def extractall(self, tempdir):
        os.system('cd %s && tar xzf %s' % (tempdir, 
                                           os.path.abspath(self.filename)))

    def close(self):
        return self.tgz.close()
 
class ZipArchive:
    def __init__(self, filename):
        self.filename = filename
        self.zipf = zipfile.ZipFile(filename, 'r')

    def names(self):
        return self.zipf.namelist()

    def lines(self, name):
        return self.zipf.read(name).split('\n')

    def extract(self, name, tempdir):
        data = self.zipf.read(name)
        fn = name.split(os.sep)[-1]
        fn = os.path.join(tempdir, fn)
        f = open(fn, 'wb')
        f.write(data)

    def extractall(self, tempdir):
        os.system('cd %s && unzip %s' % (tempdir, 
                                         os.path.abspath(self.filename)))

    def close(self):
        return self.zipf.close()

def _extractNameVersion(filename, tempdir):
    print 'Parsing:', filename

    archive = None
    
    if filename.endswith('.gz') or filename.endswith('.tgz'):
        archive = TarArchive(filename)

    elif filename.endswith('.egg') or filename.endswith('.zip'):
        archive = ZipArchive(filename)
    
    if archive is None:
        return
    try:
        for name in archive.names():
            if len(name.split('/'))==2  and name.endswith('PKG-INFO'):

                project, version = None, None

                lines = archive.lines(name)

                for line in lines:
                    key, value = line.split(':', 1)

                    if key == 'Name':
                        print filename, value
                        project = value.strip()

                    elif key == 'Version':
                        version = value.strip()

                    if project is not None and version is not None:
                        return project, version
                contiue;
                
        # no PKG-INFO found, do it the hard way.
        archive.extractall(tempdir)
        dirs = os.listdir(tempdir)
        dir = os.path.join(tempdir, dirs[0])
        if not os.path.isdir(dir):
            dir = tempdir
        command = ('cd %s && %s setup.py --name --version'
                   % (dir, sys.executable))
        popen = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 shell=True,
                                 )
        output = popen.communicate()[0]
        archive.close()
        return output.splitlines()[:2]
    except:
        archive.close()
        import traceback
        print traceback.format_exc()
    return
        


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    projects = {}
    for arg in argv:
        if arg.startswith('*'):
            continue
        try:
            tempdir = tempfile.mkdtemp()
            project, revision = _extractNameVersion(arg, tempdir)
            projects.setdefault(project, []).append((revision, arg))
            shutil.rmtree(tempdir)
        except:
            pass
            

    items = projects.items()
    items.sort()
    topname = 'index'

    if not os.path.exists(topname):
        os.makedirs(topname)
    top = open('%s/index.html' % topname, 'w')
    top.writelines(['<html>\n',
                    '<body>\n',
                    '<h1>Package Index</h1>\n',
                    '<ul>\n'])

    for key, value in items:
        print 'Project: %s' % key
        dirname = '%s/%s' % (topname, key)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        top.write('<li><a href="%s/index.html">%s</a>\n' % (key, key))

        sub = open('%s/%s/index.html' % (topname, key), 'w')
        sub.writelines(['<html>\n',
                        '<body>\n',
                        '<h1>%s Distributions</h1>\n' % key,
                        '<ul>\n'])

        for revision, archive in value:
            print '  -> %s, %s' % (revision, archive)
            sub.write('<li><a href="../../%s">%s</a>\n' % (archive, archive))

        sub.writelines(['</ul>\n',
                        '</body>\n',
                        '</html>\n'])

    top.writelines(['</ul>\n',
                    '</body>\n',
                    '</html>\n'])
    top.close()

if __name__ == '__main__':
    main()
