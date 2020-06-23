
def test_get_cases_pinned_variant(real_variant_database, case_obj, user_obj,
                                  institute_obj):
    adapter = real_variant_database

    # GIVEN that the database is populated with a case with a variant
    variant_obj=adapter.variant_collection.find_one()

    # GIVEN that variant is pinned (marked suspect)
    adapter.pin_variant(
        institute=institute_obj,
        case=case_obj,
        user=user_obj,
        link='dummy',
        variant=variant_obj,
    )

    print("Variant obj: {}".format(variant_obj))
    # WHEN searching for cases with pinned genes in the gene symbol of the pinned gene
    variant_hgnc_ids = variant_obj.get('hgnc_ids')
    variant_hgnc_id = variant_hgnc_ids[0]
    print(variant_hgnc_id)
    variant_gene = adapter.hgnc_gene(hgnc_identifier=variant_hgnc_id)
    variant_gene_symbol = variant_gene['hgnc_symbol']

    name_query= "pinned:{}".format(variant_gene_symbol)

    # THEN one case should be returned
    cases = list(adapter.cases(collaborator=case_obj['owner'], name_query=name_query))
    assert len(cases) == 1
