# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from gpu_hello_world.gpu_hello_worldImpl import gpu_hello_world
from gpu_hello_world.gpu_hello_worldServer import MethodContext
from gpu_hello_world.authclient import KBaseAuth as _KBaseAuth

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.WorkspaceClient import Workspace


class gpu_hello_worldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('gpu_hello_world'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'gpu_hello_world',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = gpu_hello_world(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa
        # cls.prepareTestData()

    @classmethod
    def prepareTestData(cls):
        pass
        """This function creates an assembly object for testing"""
        # fasta_content = '>seq1 something soemthing asdf\n' \
        #                 'agcttttcat\n' \
        #                 '>seq2\n' \
        #                 'agctt\n' \
        #                 '>seq3\n' \
        #                 'agcttttcatgg'
        #
        # filename = os.path.join(cls.scratch, 'test1.fasta')
        # with open(filename, 'w') as f:
        #     f.write(fasta_content)
        # assemblyUtil = AssemblyUtil(cls.callback_url)
        # cls.assembly_ref = assemblyUtil.save_assembly_from_fasta({
        #     'file': {'path': filename},
        #     'workspace_name': cls.wsName,
        #     'assembly_name': 'TestAssembly'
        # })

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_run_gpu_hello_world_ok(self):
        # call your implementation
        ret = self.serviceImpl.run_gpu_hello_world(self.ctx,
                                                {'workspace_name': self.wsName,
                                                 'assembly_input_ref': 1,
                                                 'min_length': 10
                                                 })

        # Validate the returned data
        self.assertEqual(ret[0]['n_initial_contigs'], 3)
        self.assertEqual(ret[0]['n_contigs_removed'], 1)
        self.assertEqual(ret[0]['n_contigs_remaining'], 2)

