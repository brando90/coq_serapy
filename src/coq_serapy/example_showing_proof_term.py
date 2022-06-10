from pprint import pprint

from pathlib import Path

import coq_serapy


# A main function demonstrating some of the features of the coq_serapy module

# To properly run this example, you need Coq installed (versions 8.9-8.12) and
# Coq Serapi installed. Then, copy this into the folder *above* the coq_serapy
# module.
def main():
    # proof_commands = [
    #     "Theorem t: forall n: nat, 1 + n > n.",
    #     "Proof.",
    #     "Show Proof.",
    #     "Proof.",
    #     "Show Proof.",
    #     "intro.",
    #     "Show Proof.",
    #     "omega.",
    #     "Show Proof.",
    #     "Qed."]
    # proof_commands = [
    #     "Theorem add_easy_0: forall n: nat, 0 + n = n.",
    #     "Proof.",
    #     "Show Proof.",
    #     "intros.",
    #     "Show Proof.",
    #     "simpl.",
    #     "Show Proof.",
    #     "reflexivity.",
    #     "Show Proof.",
    #     "Qed.",
    # ]
    # You can also load commands from a file, like this:
    #
    # proof_commands = coq_serapy.load_commands(<filename>)
    #    OR
    # proof_commands = coq_serapy.read_commands(<string>)
    debug_proj_path: Path = Path('~/coq_serapy/debug_proj/').expanduser()
    filename: str = 'debug_0_plus_n_eq_n.v'
    # filename: str = 'debug1_n_plus_1_less_than_n.v'
    # filename: str = 'debug2_n_plus_0_eq_n.v'
    debug_coqfile_path: Path = debug_proj_path / filename
    proof_commands = coq_serapy.load_commands(debug_coqfile_path)
    pprint(f'{proof_commands=}')

    with coq_serapy.SerapiContext(
            # How you want the underlying sertop binary to be run. If not sure,
            # use this.
            coq_commands=["sertop", "--implicit"],
            # A top level module for the code to reside in. Empty string or
            # None leaves in the default top module.
            module_name=coq_serapy.get_module_from_filename(filename),
            # A prelude directory in which to start the binary
            prelude=str(debug_proj_path)) as coq:
    # with coq_serapy.SerapiContext(
    #         # How you want the underlying sertop binary to be run. If not sure,
    #         # use this.
    #         ["sertop", "--implicit"],
    #         # A top level module for the code to reside in. Empty string or
    #         # None leaves in the default top module.
    #         "MyModule",
    #         # A prelude directory in which to start the binary
    #         ".") as coq:
        print(f'{coq=}')

        # Runs commands from a list until we enter a proof, then returns a
        # tuple of (commands-left-over, commands-that-were-run)
        cmds_left, cmds_run = coq.run_into_next_proof(proof_commands)
        print(f'{cmds_left=}')
        print(f'{cmds_run=}')
        print()
        # assert cmds_run == ["Theorem t: forall n: nat, 1 + n > n."], cmds_run
        # assert cmds_left == [
        #     "Proof.",
        #     "intro.",
        #     "omega.",
        #     "Qed."], cmds_left

        # Print out the proof context
        print(coq.proof_context)

        # Setting this makes sure that coq doesn't print extra on failed
        # commands. Without it, failed proofs will get a message printed to
        # standard out, even if you catch the exception.
        coq.quiet = True

        try:
            _, _ = coq.finish_proof(cmds_left)
        except coq_serapy.CoqExn:
            # Oops! We forgot to import omega."
            # Back out of the proof and import it.
            while coq.proof_context:
                coq.cancel_last()
            coq.run_stmt("Require Import Omega.")
            cmds_left, cmds_run = coq.run_into_next_proof(proof_commands)
            # Now it should finish fine
            _, _ = coq.finish_proof(cmds_left)


# Run main if this module is being run standalone
if __name__ == "__main__":
    main()
