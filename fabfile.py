from fabric.api import local, lcd, env, put

module = 'teapot'
bucket = 'b4is-apt-repo-690a0b40-60d1-4fde-a41b-3f1dcb0a28bf'

def hello():
    print("Hello world!")


def clean() :
    with lcd('..') :
        local( "rm -f %s_*"%module )
        local( "rm -f *.deb" )

def build() :
    clean()
    local("dpkg-buildpackage -kB26BF320")

def install() :
    local( 'sudo dpkg -r %s'%module )
    with lcd('..') :
       local( 'sudo dpkg -i %s_*.deb'%module )


def post_local() :
    build()
    with lcd('/var/repos') :
       local( 'reprepro --ask-passphrase  -Vb . includedeb sid /home/artb/projects/teapot_*_amd64.deb') 

def post() :
    with lcd('..') :
       local( 's3cmd --verbose --delete-removed --follow-symlinks  sync /var/repos/ s3://%s/'%bucket) 
 

def reinstall() :
    clean()
    build()
    install()    
