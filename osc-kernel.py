from osc import core, cmdln
try:
	from xml.etree import cElementTree as ET
except ImportError:
	import cElementTree as ET

def log_url(self, project, repository, arch, package):
	return core.makeurl(conf.config['apiurl'], ['build', project, repository, arch, package, '_log'])

def get_kernel_package(self, project, package="kernel-default"):
	return [x for x in core.get_package_results(conf.config['apiurl'], project, package) if '_oldstate' not in x]

def get_kernel_version(self, project, package, repository, arch):
	buildinfo_xml = core.get_buildinfo(conf.config['apiurl'], project, package, repository, arch)
	buildinfo_tree = ET.fromstring(buildinfo_xml)
	return buildinfo_tree.find("versrel").text

def get_kernel_project(self, project, package):
	ret = {}
	fails = []
	version = None

	for x in self.get_kernel_package(project, package):
		out = x['code']
		if x['code'] == 'succeeded':
			if version == None:
				version = self.get_kernel_version(x['prj'], x['pac'], x['rep'], x['arch'])
			out = version
		if x['code'] == 'failed':
			fails.append(self.log_url(x['prj'], x['rep'], x['arch'], x['pac']))
		if x['code'] == 'disabled':
			continue
		ret[x['arch']] = out

	return (ret, fails)

def format_table(self, archs, projects):
	a = max([len(x) for x in archs])
	p = [len(x) for x in projects]
	w = [a] + p
	return "\t".join(['{{{0}:<{1}}}'.format(*x) for x in enumerate(w)])

@cmdln.alias('ks')
@cmdln.option('-p', '--project', action='append', help='specify one or more projects to show')
@cmdln.option('-a', '--arch', action='append', help='specify one or more archs to show')
@cmdln.option('--package', action='store', default='kernel-default', help='specify package name to show (kernel-default is default)')
def do_kernelsummary(self, subcmd, opts):
	"""${cmd_name}: Show summary of the kernel packages

	This command shows the summary of the kernel packages status.
    
	${cmd_usage}
	${cmd_option_list}
	"""

	projects = ["Kernel:HEAD", "Kernel:stable", "Kernel:openSUSE-13.2"]
	archs = ["i586", "x86_64", "armv6l", "armv7l", "aarch64", "ppc", "ppc64"]
	if opts.project:
		projects = opts.project
	if opts.arch:
		archs = opts.arch

	fmt = self.format_table(archs, projects)

	res = dict([(p, self.get_kernel_project(p, opts.package)) for p in projects])

	print "Kernel summary:"
	print fmt.format("",*projects)
	for a in archs:
		print fmt.format(a,*([res[p][0].get(a,"") for p in projects]))

	print
	print "Failed packages:"
	for (x,fails) in res.values():
		for f in fails:
			print f

