# -*- coding: utf-8 -*-

"""Template database models"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

TABLE_PREFIX = 'compath_template'  # TODO: Change name
PATHWAY_TABLE_NAME = '{}_pathway'.format(TABLE_PREFIX)
PROTEIN_TABLE_NAME = '{}_protein'.format(TABLE_PREFIX)
PROTEIN_PATHWAY_TABLE = '{}_protein_pathway'.format(TABLE_PREFIX)

protein_pathway = Table(
    PROTEIN_PATHWAY_TABLE,
    Base.metadata,
    Column('protein_id', Integer, ForeignKey('{}.id'.format(PROTEIN_TABLE_NAME)), primary_key=True),
    Column('pathway_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)), primary_key=True)
)


class Pathway(Base):
    """Pathway Table"""

    __tablename__ = PATHWAY_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255), unique=True, index=True, nullable=False, doc='pathway name')

    proteins = relationship(
        'Protein',
        secondary=protein_pathway,
        backref='pathways'
    )

    def __repr__(self):
        return self.name

    def get_gene_set(self):
        """Returns the genes associated with the pathway (gene set). Note this function restricts to HGNC symbols genes

        :rtype: set[compath_template.models.Protein]
        """
        return {
            protein
            for protein in self.proteins
            if protein.hgnc_symbol
        }

class Protein(Base):
    """Genes Table"""

    __tablename__ = PROTEIN_TABLE_NAME

    id = Column(Integer, primary_key=True)

    hgnc_symbol = Column(String(255), unique=True, index=True, nullable=False, doc='hgnc symbol of the protein')

    def __repr__(self):
        return self.hgnc_symbol
