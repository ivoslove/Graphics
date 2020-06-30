from ..shared.namer import packages_filepath
from .package_pack import Package_PackJob
from .package_publish import Package_PublishJob
from .package_test import Package_TestJob
from .package_test_dependencies import Package_TestDependenciesJob
from .package_publish_all import Package_PublishAllJob
from .package_test_all import Package_AllPackageCiJob


def create_package_ymls(metafile):

    yml_files = {}
    yml = {}

    for package in metafile["packages"]:
        job = Package_PackJob(package, metafile["agent_pack"])
        yml[job.job_id] = job.yml

        job = Package_PublishJob(package, metafile["agent_publish"], metafile["platforms"], metafile["target_editor"])
        yml[job.job_id] = job.yml

    for editor in metafile["editors"]:
        for platform in metafile["platforms"]:
            for package in metafile["packages"]:
                job = Package_TestJob(package, platform, editor)
                yml[job.job_id] = job.yml

                job = Package_TestDependenciesJob(package, platform, editor)
                yml[job.job_id] = job.yml

    for editor in metafile['editors']:
        job = Package_AllPackageCiJob(metafile["packages"], metafile["agent_publish"], metafile["platforms"], editor)
        yml[job.job_id] = job.yml
    
    job = Package_PublishAllJob(metafile["packages"], metafile["agent_publish_all"])
    yml[job.job_id] = job.yml

    yml_files[packages_filepath()] = yml
    return yml_files