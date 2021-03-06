/*
 * Copyright � 2008 UChicago Argonne, LLC
 * NOTICE: This computer software, TEVA-SPOT, was prepared for UChicago Argonne, LLC
 * as the operator of Argonne National Laboratory under Contract No. DE-AC02-06CH11357
 * with the Department of Energy (DOE). All rights in the computer software are reserved
 * by DOE on behalf of the United States Government and the Contractor as provided in
 * the Contract.
 * NEITHER THE GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR
 * ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.
 *
 * This software is distributed under the BSD License.
 */
/* DO NOT EDIT THIS FILE - it is machine generated */
#include <jni.h>
/* Header for class anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl */

#ifndef _Included_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
#define _Included_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
#ifdef __cplusplus
extern "C" {
#endif
/*
 * Class:     anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
 * Method:    getResults
 * Signature: (Lanl/teva/analysis/module/NamedDataServer;Lanl/teva/analysis/module/AnalysisResults;)V
 */
JNIEXPORT void JNICALL Java_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl_getResults
  (JNIEnv *, jobject, jlong, jobject, jobject);

/*
 * Class:     anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
 * Method:    init
 * Signature: (Lanl/teva/analysis/module/NamedDataServer;)V
 */
JNIEXPORT void JNICALL Java_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl_init
  (JNIEnv *, jobject, jlong, jobject, jobject);

/*
 * Class:     anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
 * Method:    shutdown
 * Signature: (Lanl/teva/analysis/module/NamedDataServer;)V
 */
JNIEXPORT void JNICALL Java_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl_shutdown
  (JNIEnv *, jobject, jlong, jobject);

/*
 * Class:     anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
 * Method:    newResults
 * Signature: (Lanl/teva/analysis/module/NamedDataServer;Lanl/teva/analysis/module/NamedData;)V
 */
JNIEXPORT void JNICALL Java_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl_newResults
  (JNIEnv *, jobject, jlong, jobject, jobject);

/*
 * Class:     anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl
 * Method:    newResults
 * Signature: (Lanl/teva/analysis/module/NamedData;)V
 */
JNIEXPORT jstring JNICALL Java_anl_teva_analysis_module_ExternalAnalysisAggregationServerImpl_writeResults
  (JNIEnv *, jobject, jlong, jobject, jobject, jstring);

#ifdef __cplusplus
}
#endif
#endif
