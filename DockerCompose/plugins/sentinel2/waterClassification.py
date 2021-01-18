from eodatadown.eodatadownuseranalysis import EODataDownUserAnalysis
from eodatadown.eodatadownutils import EODataDownUtils

import rsgislib
import rsgislib.imagecalibration
import rsgislib.imagecalc
import rsgislib.imagecalc.calcindices
import rsgislib.vectorutils

import logging
import os
import shutil

logger = logging.getLogger(__name__)


class waterClassification(EODataDownUserAnalysis):

    def __init__(self):
        #logger.info("Test plugin starting")
        usr_req_keys = ["tmp_path"]
        EODataDownUserAnalysis.__init__(self, analysis_name='test', req_keys=usr_req_keys)

    def perform_analysis(self, scn_db_obj, sen_obj, plgin_objs):
        success = True
        out_info = None
        out_file_present = True
        try:
            rsgis_utils = rsgislib.RSGISPyUtils()
            eodd_utils = EODataDownUtils()
            
            # Find masked image file
            valid_img_file = rsgis_utils.findFileNone(scn_db_obj.ARDProduct_Path, "*_vmsk_mclds_topshad_rad_srefdem_stdsref.tif")
            print("valid image file: " , valid_img_file)

            # Base name for files
            basename = rsgis_utils.get_file_basename(valid_img_file)
            basename = basename.replace('_v', '')
            logger.debug("The basename for the processing is: {}".format(basename))

            # Create tmp dir
            base_tmp_dir = os.path.join(self.params["tmp_path"], "{}_{}_water".format(scn_db_obj.Product_ID, scn_db_obj.PID))
            if not os.path.exists(base_tmp_dir):
                os.mkdir(base_tmp_dir)

            # Create water kea file
            water_img = os.path.join(base_tmp_dir, "{}_water.kea".format(basename))
            maths='b5>0?b5<50:0'
            rsgislib.imagecalc.imageBandMath(valid_img_file,water_img,maths,"KEA",rsgislib.TYPE_32FLOAT)
            rsgislib.imageutils.popImageStats(water_img, usenodataval=True, nodataval=0, calcpyramids=True)

            # Polygonise
            water_vector = os.path.join(scn_db_obj.ARDProduct_Path, "{}_water.gpkg".format(basename))
            rsgislib.vectorutils.polygoniseRaster2VecLyr(water_vector,'water','GPKG',water_img)

            # Create water geotiff in ARD product path
            water_tif_img = eodd_utils.translateCloudOpGTIFF(water_img, scn_db_obj.ARDProduct_Path)

            # Clean up tmp directory
            if os.path.exists(base_tmp_dir):
                shutil.rmtree(base_tmp_dir)

            out_info = {"water_img": water_tif_img}

        except Exception as e:
            logger.debug("An error occurred during plugin processing. See stacktrace...", stack_info=True)
            logger.exception(e)
            success = False
            out_file_present = False
        
        print(success)
        return success, out_info, out_file_present



