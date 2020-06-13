# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
	/////////////////////////////////////////////////////////////////////////
	//
	// (c) Copyright University of Southampton, 2020
	//
	// This software may not be used, sold, licensed, transferred, copied
	// or reproduced in whole or in part in any manner or form or in or
	// on any media by any person other than in accordance with the terms
	// of the Licence Agreement supplied with the software, or otherwise
	// without the prior written consent of the copyright owners.
	//
	// This software is distributed WITHOUT ANY WARRANTY, without even the
	// implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
	// PURPOSE, except where stated in the Licence Agreement supplied with
	// the software.
	//
	// Created By : Stuart E. Middleton
	// Created Date : 2020/05/18
	// Created for Project : FloraGuard
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies : None
	//
	/////////////////////////////////////////////////////////////////////////
	'''

"""

__all__ = ["lexicon_lib", "lexicon_bootstrapping_lib", "wordnet_lib" ]

# note: lexicon_lib should be imported first as others may depend on it
import soton_corenlppy.lexico.lexicon_lib
import soton_corenlppy.lexico.lexicon_bootstrapping_lib
import soton_corenlppy.lexico.wordnet_lib
