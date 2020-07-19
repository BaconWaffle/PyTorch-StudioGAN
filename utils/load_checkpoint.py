# PyTorch StudioGAN: https://github.com/POSTECH-CVLab/PyTorch-StudioGAN
# The MIT License (MIT)
# See license file or visit https://github.com/POSTECH-CVLab/PyTorch-StudioGAN for details

# utils/load_checkpoint.py


import torch

import os



def load_checkpoint(model, optimizer, filename, metric=False, ema=False):
    # Note: Input model & optimizer should be pre-defined.  This routine only updates their states.
    start_step = 0
    if os.path.isfile(filename):
        if ema:
            checkpoint = torch.load(filename)
            model.load_state_dict(checkpoint['state_dict'])
            return model
        else:
            checkpoint = torch.load(filename)
            seed = checkpoint['seed']
            run_name = checkpoint['run_name']
            start_step = checkpoint['step']
            best_step = checkpoint['best_step']
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            for state in optimizer.state.values():
                for k, v in state.items():
                    if isinstance(v, torch.Tensor):
                        state[k] = v.cuda()

            if metric:
                best_fid = checkpoint['best_fid']
                best_fid_checkpoint_path = checkpoint['best_fid_checkpoint_path']
                return model, optimizer, seed, run_name, start_step, best_step, best_fid, best_fid_checkpoint_path
    else:
        raise FileNotFoundError
    return model, optimizer, seed, run_name, start_step, best_step
