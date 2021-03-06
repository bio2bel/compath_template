# -*- coding: utf-8 -*-

"""
This module populates the tables
"""

import logging
import itertools as itt

from compath_utils import CompathManager
from bio2bel.utils import get_connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from collections import Counter

from .constants import MODULE_NAME
from .models import Base, Pathway, Protein

__all__ = [
    'Manager'
]

log = logging.getLogger(__name__)


class Manager(CompathManager):
    """Database manager"""

    module_name = MODULE_NAME

    flask_admin_models = [Pathway, Protein]
    pathway_model = Pathway
    protein_model = Protein
    pathway_model_identifier_column = Pathway.id

    @property
    def _base(self):
        return Base

    """Custom query methods"""

    def get_or_create_pathway(self, pathway_name):
        """Gets an pathway from the database or creates it

        :param str pathway_name: pathway ame
        :rtype: Pathway
        """
        pathway = self.get_pathway_by_name(pathway_name)

        if pathway is None:
            pathway = Pathway(
                name=pathway_name
            )
            self.session.add(pathway)

        return pathway

    def get_protein_by_id(self, identifier):
        """Gets a protein by its id

        :param identifier: identifier
        :rtype: Optional[Protein]
        """
        return self.session.query(Protein).filter(Protein.id == identifier).one_or_none()

    def get_or_create_protein(self, hgnc_symbol):
        """Gets an protein from the database or creates it
        :param Optional[str] hgnc_symbol: name of the protein
        :rtype: Protein
        """
        protein = self.get_protein_by_hgnc_symbol(hgnc_symbol)

        if protein is None:
            protein = Protein(
                hgnc_symbol=hgnc_symbol,
            )
            self.session.add(protein)

        return protein


    """Methods to populate the DB"""

    def _populate_pathways(self, url=None):
        """Populate pathway table

        :param Optional[str] url: url from pathway table file
        """

        # TODO: add here your parser for the pathway model (see example.py)
        pathways_dict = ...

        for id, name in tqdm(pathways_dict.items(), desc='Loading pathways'):
            pathway = self.get_or_create_pathway(pathway_name=name)

        self.session.commit()

    def _pathway_entity(self, url=None):
        """Populates Protein Tables

        :param Optional[str] url: url from protein to pathway file
        """

        # TODO: add here your parser for the protein model (see example.py)

        protein_pathway_dict = ...

        for hgnc_symbol, pathway_name in tqdm(protein_pathway_dict, desc='Loading proteins'):
            protein = self.get_or_create_protein(hgnc_symbol=hgnc_symbol)

            pathway = self.get_pathway_by_name(pathway_name)

            protein.pathways.append(pathway)

        self.session.commit()

    def populate(self, pathways_url=None, protein_pathway_url=None):
        """Populates all tables"""
        self._populate_pathways(url=pathways_url)
        self._pathway_entity(url=protein_pathway_url)
